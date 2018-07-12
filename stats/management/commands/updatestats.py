'''Updates Aircraft SQL table with data from most current slmod json.  Takes no arguments'''
import os
import json
# import glob
import datetime
from pathlib import Path
import subprocess
import pytz
import traceback
from django.core.management.base import BaseCommand, CommandError
from stats.models import Pilot, Aircraft, Mission

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

def list_files(spath):
    '''list all files in slmis folder except SlmodMetastats and SlmodStats'''
    mis_stats = []
    for root, dirs, files in os.walk(spath):
        for file in files:
            if file != 'SlmodMetaStats.lua' and file != 'SlmodStats.lua':
                mis_stats.append(file)
    return mis_stats

def update_mismodel(aircrafts, pilots, file, stats_json, date, ip_flag):
    '''Update Mission Django model from dict'''
    in_air_sec = stats_json[pilots]['times'][aircrafts.aircraft]['inAir']
    total_sec = stats_json[pilots]['times'][aircrafts.aircraft]['total']
    crash = stats_json[pilots]['losses']['crash']
    eject = stats_json[pilots]['losses']['eject']
    death = stats_json[pilots]['losses']['pilotDeath']
    friendly_col_hits = stats_json[pilots]['friendlyCollisionHits']
    friendly_col_kills = stats_json[pilots]['friendlyCollisionKills']
    friendly_hits = stats_json[pilots]['friendlyHits']
    friendly_kills = stats_json[pilots]['friendlyKills']
    building_kills = stats_json[pilots]['kills']["Buildings"]["total"]
    ground_kills = stats_json[pilots]['kills']['Ground Units']['total']
    heli_kills = stats_json[pilots]['kills']["Helicopters"]['total']
    fighter_kills = stats_json[pilots]['kills']['Planes']['Fighters']
    all_aircraft_kills = stats_json[pilots]['kills']['Planes']['total']
    ship_kills = stats_json[pilots]['kills']['Ships']['total']
    pilot = Pilot.objects.get(clientid=pilots)
    if type(friendly_kills) == list:
        friendly_kills = 0
    if type(friendly_hits) == list:
        friendly_hits = 0
    if type(friendly_col_kills) == list:
        friendly_col_kills = 0
    if type(friendly_col_hits) == list:
        friendly_col_hits = 0
    print(f'Printing from update_mismodel {file[:-30]}')
    new_mission = Mission.manager.create_entry(aircrafts,
                                               in_air_sec,
                                               total_sec,
                                               pilot,
                                               file[:-30],
                                               date,
                                               crash,
                                               eject,
                                               death,
                                               friendly_col_hits,
                                               friendly_col_kills,
                                               friendly_hits,
                                               friendly_kills,
                                               building_kills,
                                               ground_kills,
                                               heli_kills,
                                               fighter_kills,
                                               all_aircraft_kills,
                                               ship_kills, ip_flag,
                                               file
                                               )

def log(string):
    '''write string to stats/logs/DATE and print string'''
    today = datetime.date.today()
    today = today.strftime('%b %d %Y')
    file = open(Path('stats/logs/'+today+'.txt'), "a")
    time = datetime.datetime.utcnow().isoformat(' ')
    file.write(f'{time} : ' + string + '\n')
    print(string)

def mis_update():
    '''
    Update Mission Django model from json
    '''
    curdate = datetime.datetime.now()
    curdate = curdate.strftime('%b %d %Y %H%M%S')
    log_path = Path('stats/logs/' + curdate + '.txt')
    log('START UPDATE:')
    print("Scanning stats folder")
    #Check for already converted slmod mission luas
    mpath = Path('slmod/')
    mis_stats = list_files(mpath)
    exclude = []
    p_slmis = Path('stats/processed_slmis.txt')
    try:
        with open(p_slmis, "r") as processed_slmis:
            for line in processed_slmis:
                exclude.append(line[:-1])
        processed_slmis.close()
    except FileNotFoundError:
        pass
    new_count = len(mis_stats)-len(exclude)
    if new_count < 0:
        new_count = 0
    else:
        pass
    print(f"Converting {new_count} SlMod mission files to JSON")
    slmis_lua = Path('lua/src/slmisconvert.lua')
    processed_slmis = open(p_slmis, "a")
    ip_path = Path('stats/in_process.txt')
    ip_list = []
    try:
        with open(ip_path, "r") as ip_file:
            for line in ip_file:
                ip_list.append(line[:-1])
        ip_file.close()
    except FileNotFoundError:
        pass
    progress = 0
    for m in mis_stats:
        if m in exclude:
            pass
        else:
            progress += 1
            print(f'Converting {progress} of {new_count} to JSON')
            curmispath = Path(mpath / m)
            with open(curmispath) as curmisfile:
                first_line = curmisfile.readline()
                curmisfile.close()
            if 'misStats = { }' in first_line:
                ip_list.append(m[:-4])
                final = False
            else:
                final = True
                if m in ip_list:
                    ip_list.remove(m)
                ip_string = ''    
                for l in ip_list:
                    ip_string += l + '\n'
            print(f'Printing final at line 156 {final}')
            if final:
                process = f'lua {slmis_lua} "{mpath}/{m}" "/{m[:-4]}"'
                subprocess.call(process, shell=True)
                processed_slmis.write(m + "\n")
                log(f'NEW JSON: {m}')
            else:
                process = f'lua {slmis_lua} "{mpath}/{m}" "/{m[:-4]}"'
                subprocess.call(process, shell=True)
                log(f'NEW IN_PROCESS JSON: {m}')
    processed_slmis.close()
    print("Finished Lua conversions")
    #Check for already imported slmod mission JSONs
    print("Scanning JSONs")
    spath = Path("slmis")
    new_files = list_files(spath)
    # pilot_list = get_pilots()
    exclude = []
    finishedpath = Path('stats/finishedfiles.txt')
    try:
        with open(finishedpath, "r") as finishedfiles:
            for line in finishedfiles:
                exclude.append(line[:-1])
        finishedfiles.close()
    except FileNotFoundError:
        pass
    new_count = len(new_files)-len(exclude)
    if new_count < 0:
        new_count = 0
    else:
        pass
    print(f'Found {new_count} new files to import')
    #Import new JSONs to Django Mission Model
    progress = 0
    error_list = []
    for file in new_files:
        if file in exclude:
            pass
        else:
            progress += 1
            print(f'Importing {progress} of {new_count}')
            lua_suff = file[:-5] + ".lua"
            lua_name = mpath / lua_suff
            date = datetime.datetime.fromtimestamp(os.path.getmtime(lua_name), pytz.UTC)
            filename = Path(spath / file)
            stats_json = load_json(filename)
            pilot_list = []
            if stats_json != []:
                if file[:-5] not in ip_list:
                    ip_flag = 1
                else:
                    ip_flag = 0
                for client in stats_json:
                    try:
                        callsign = stats_json[client]['names'][0]
                    except IndexError:
                        callsign = 'None' 
                    try:                   
                        pilot_list.append(Pilot.objects.get(clientid=client).clientid)
                    except:
                        traceback.print_exc()
                        new_pilot = Pilot.objects.create(clientid=client, callsign=callsign)
                        new_pilot = Pilot.objects.get(clientid=client)
                        pilot_list.append(new_pilot)
                        log(f'NEW PILOT: {new_pilot.clientid} Callsign={new_pilot.callsign}')
                print(f'Printing final at line 221 {final} \nPrinting file {file}')
                for p in pilot_list:
                    try:
                        for k in stats_json[p]['times'].keys():
                            new_aircraft = Aircraft.objects.get_or_create(aircraft=k)
                            if new_aircraft[1] == True:
                                log(f'NEW AIRCRAFT: {new_aircraft[0].aircraft}')
                            new_aircraft = Aircraft.objects.get(aircraft=k)
                            print(f'Printing from line 228 {file}')
                            update_mismodel(new_aircraft, p, file, stats_json, date, ip_flag)

                    except KeyError as e:
                        pass
                    except AttributeError as e:
                        pass
                if ip_flag:
                    with open(finishedpath, 'a') as finishedfiles:
                        finishedfiles.write(file + '\n')
                    finishedfiles.close()
                log(f'IMPORTED: {file}')
            else:
                error_list.append(filename)
                log(f'FAILED IMPORT: {filename} contains no data')
    log(f"FINISH UPDATE: {len(error_list)} errors")


def delete_mission():
    '''Delete all stats in mission table and clear finishedfiles.txt and processed_slmis.txt'''
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
            help='Deletes all records in Mission table')
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
            return mis_update()
