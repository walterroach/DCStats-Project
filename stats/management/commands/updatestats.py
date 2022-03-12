'''Updates Aircraft SQL table with data from most current slmod json.  Takes no arguments'''
import os
import json
import datetime
from pathlib import Path
import subprocess
import pytz
from django.core.management.base import BaseCommand, CommandError
from stats.models import Pilot, Aircraft, Stats, Mission

def load_json(fpath):
    '''load json at fpath and return dict'''
    stats_file = open(fpath)
    stats_json = stats_file.read()
    stats_json = json.loads(stats_json)
    stats_file.close()
    return stats_json

def get_pilots():
    '''fetch all clientids in Pilot model and return list'''
    pilots = Pilot.objects.all()
    pilot_list = []
    for pilot in pilots:
        pilot_list.append(pilot.clientid)
    return pilot_list

def list_files(dir_path, exclusions):
    '''list all files in dir, return as list of dicts {file:modified_date}'''
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file not in exclusions:
                filepath = Path(dir_path / file)
                mod_date = datetime.datetime.fromtimestamp(os.path.getmtime(filepath),
                                                           pytz.UTC)
                file_list.append({'file':file, 'date':mod_date})
            else:
                pass
    return file_list

def log(string):
    '''write string to stats/logs/DATE and print string'''
    today = datetime.date.today()
    today = today.strftime('%b %d %Y')
    try:
        file = open(Path('stats/logs/'+today+'.txt'), "a")
    except FileNotFoundError:
        os.mkdir("stats/logs")
        file = open(Path('stats/logs/'+today+'.txt'), "a")
    time = datetime.datetime.utcnow().isoformat(' ')
    file.write(f'{time} : ' + string + '\n')
    print(string)

def update_models(key,
                  pilot,
                  filename,
                  mission,
                  stats_json,
                  date,
                  in_process):
    '''get_or_create aircraft, mission, and stats objects'''
    new_aircraft = Aircraft.objects.get_or_create(aircraft=key)
    if new_aircraft[1]:
        log(f'NEW AIRCRAFT:  {new_aircraft[0].aircraft}')
    new_aircraft = new_aircraft[0]
    model_pilot = Pilot.objects.get(clientid=pilot)
    new_mission = Mission.objects.get_or_create(file=filename)
    if new_mission[1]:
        new_mission[0].name = mission
        new_mission[0].date = date
        log(f'NEW MISSION : {new_mission[0]}')
    expire = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    expire = pytz.utc.localize(expire)
    if in_process:
        if date < expire:
            in_process = 0
            log(f'IN PROCESS OFF : {new_mission[0]}')
    new_mission[0].in_process = in_process
    new_mission = new_mission[0]
    new_mission.save()
    stats = Stats.objects.get_or_create(mission=new_mission,
                                        pilot=model_pilot,
                                        aircraft=new_aircraft,
                                       )
    stats = stats[0]
    stats.in_air_sec = stats_json[pilot]['times'][new_aircraft.aircraft]['inAir']
    stats.total_sec = stats_json[pilot]['times'][new_aircraft.aircraft]['total']
    
    crash = stats_json[pilot]['losses']['crash']
    eject = stats_json[pilot]['losses']['eject']
    death = stats_json[pilot]['losses']['pilotDeath']
    stats.losses = crash + eject + death

    building_kills = stats_json[pilot]['kills']["Buildings"]["total"]
    ground_kills = stats_json[pilot]['kills']['Ground Units']['total']
    
    stats.ground_kills = ground_kills + building_kills
    all_aircraft_kills = stats_json[pilot]['kills']['Planes']['total']

    stats.aircraft_kills = all_aircraft_kills

    ship_kills = stats_json[pilot]['kills']['Ships']['total']
    stats.ship_kills = stats_json[pilot]['kills']['Ships']['total']
    stats.save()

def stats_update():
    log('START UPDATE :')
    ## Create list of already processed SLMod Mission .lua files
    all_missions = Mission.objects.all()
    finished_missions = Mission.objects.filter(in_process=0)
    exclusions = ['SlmodMetaStats.lua', 'SlmodStats.lua']
    for mission in finished_missions:
        exclusions.append(mission.file)
    sl_lua_path = Path('slmod/')
    ## Convert all unprocessed SLMod Mission .luas to JSON
    file_list = list(list_files(sl_lua_path, exclusions))
    print(f'FILE LIST: {len(file_list)}')
    slmis_lua = Path('lua/src/slmisconvert.lua')
    total_failed = []
    for file in file_list:
        filepath = Path(sl_lua_path / file['file'])
        filename = file['file']
        date = file['date']
        mission = filename[:-4]
        with open(filepath) as curmisfile:
            first_line = curmisfile.readline()
            curmisfile.close()
        process = f'lua {slmis_lua} "{sl_lua_path}/{filename}" "/{mission}"'
        subprocess.call(process, shell=True)
        log(f'LUA CONVERSION : {filename}')
        if 'misStats = { }' in first_line:
            in_process = 1
        else:
            in_process = 0
        ## Load json to memory
        filepath = Path('slmis/' + mission + '.json')
        with open(filepath) as curjson:
            stats_json = curjson.read()
            stats_json = json.loads(stats_json)
            curjson.close()
        if stats_json == []:
            log(f'FAILED IMPORT: {curjson} contains no data')
            total_failed.append(curjson)
        ## Check if pilots in json exist in db, create if not.
        else:
            pilot_list = []
            for client in stats_json:
                ###TODO This skips admin entries, make configurable for different servers
                if client != 'd3e5193a19b7b4a5b3468492c7184a63':
                    try:
                        callsign = stats_json[client]['names'][0]
                    except IndexError:
                        callsign = 'None'
                    try:
                        pilot_list.append(Pilot.objects.get(clientid=client).clientid)
                    except:
                        new_pilot = Pilot.objects.create(clientid=client, callsign=callsign)
                        new_pilot = Pilot.objects.get(clientid=client)
                        pilot_list.append(new_pilot.clientid)
            ## Check if aircraft in json exist in db, create if not.
            print(pilot_list)
            for pilot in pilot_list:
                try:
                    for key in stats_json[pilot]['times'].keys():
                        update_models(key,
                                      pilot,
                                      filename,
                                      mission[:-26],
                                      stats_json,
                                      date,
                                      in_process)

                except AttributeError as e:
                    stats_json[pilot]['times'] = {'None' : {"inAir":0, "total":0}}
                    for key in stats_json[pilot]['times'].keys():
                        update_models(key,
                                      pilot,
                                      filename,
                                      mission[:-26],
                                      stats_json,
                                      date,
                                      in_process)

            log(f'IMPORTED : {filename}')
    print(len(total_failed))

def delete_mission():
    '''Delete all stats in mission table and clear finishedfiles.txt and processed_slmis.txt'''
    Stats.objects.all().delete()
    Mission.objects.all().delete()
    with open('stats/finishedfiles.txt', "w") as finishedfiles:
        finishedfiles.close()
    with open('stats/processed_slmis.txt', "w") as processed_slmis:
        processed_slmis.close()
    with open('stats/in_process.txt', "w") as in_progress:
        in_progress.close()


def delete_aircraft():
    '''delete all records in Aircraft table'''
    Aircraft.objects.all().delete()

def list_aircraft():
    '''queryset for all aircraft'''
    aircrafts = Aircraft.objects.all()

class Command(BaseCommand):
    '''
    Handle updatestats options, if no option update all mission stats
    '''
    def add_arguments(self, parser):
        parser.add_argument(
            '--deletemission',
            action='store_true',
            dest='deletemission',
            help='Deletes all records in Stats table')
        parser.add_argument(
            '--deleteaircraft',
            action='store_true',
            dest='deleteaircraft',
            help='Deletes all records in aircraft table')
        parser.add_argument(
            '--list_aircraft',
            action='store_true',
            dest='list_aircraft',
            help='lists all records in aircraft table')
    def handle(self, **options):
        if options['deletemission']:
            valid = False
            while not valid:
                cont = input('This will remove all stats data from the database'
                             ' and cannot be undone.  '
                             'Are you sure you want to delete all missions?  y/n')
                if cont.lower() == 'y' or cont.lower() == 'n':
                    valid = True
            if cont.lower() == 'y':
                return delete_mission()
            else:
                print('aborted')
        elif options['deleteaircraft']:
            return delete_aircraft()
        elif options['list_aircraft']:
            return list_aircraft()
        else:
            return stats_update()
