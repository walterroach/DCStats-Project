'''Updates Aircraft SQL table with data from most current slmod json.  Takes no arguments'''
import os
import json
import glob
import datetime
import subprocess
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

def update_stats():
    '''Update Aircraft SQL table with data from most current slmod json'''

    #Clear exsiting aircraft database.
    aircraft = Aircraft.objects.all().delete()

    #Finds and loads most recent stats_YYYY_MM_DD_TTTT.json file
    try:
        dir_path = os.getcwd() + '\\slmod'
    except:
        dir_path = os.getcwd() +'/slmod'

    list_of_files = glob.glob(dir_path + '\\*')
    fpath = max(list_of_files, key=os.path.getctime)

    stats_json = load_json(fpath)

    #Fetches current active users from Pilot SQL table
    pilot_list = get_pilots()

    #Updates aircraft database with new data
    for p in pilot_list:
        for k in stats_json[p]['times'].keys():
            aircraft = k
            in_air_sec = stats_json[p]['times'][k]['inAir']
            total_sec = stats_json[p]['times'][k]['total']
            pilot = Pilot.objects.get(clientid=p)
            new_aircraft = Aircraft.manager.create_entry(aircraft,
                                                        in_air_sec, total_sec, pilot)
     

    print(f'Updated totals for clients {pilot_list}')
    return 'done'

def mis_update():
    '''
    Updates Mission Django model from json
    '''
    print("Scanning stats folder")
    mis_stats = []
    spath = 'D:\\DCS\\Willshouse\\stats'
    for root, dirs, files in os.walk(spath):
        for file in files:
            if file.endswith('.lua'):
                if file != 'SlmodMetaStats.lua' and file != 'SlmodStats.lua':
                    mis_stats.append(file)
    stats_dates = []
    print('Creating timestamps from filenames')
    exclude = []

    try:        
        with open('stats\\processed_slmis.txt', "r") as processed_slmis:
            for line in processed_slmis:
                exclude.append(line[:-1])
        processed_slmis.close()
    except FileNotFoundError:
        pass

    for m in mis_stats:
        if m in exclude:
            continue
        else:
            date_str = m[-28:-4]
            date = datetime.datetime.strptime(date_str, "%b %d, %Y at %H %M %S")
            date = date.strftime('%b %d, %Y at %H %M %S')
            s_d = (m,date)
            stats_dates.append(s_d)
    print(f'Found {len(stats_dates)} SlMod Mission Files')
    print(f"Converting {len(stats_dates)} SlMod mission files to JSON")

    processed_slmis = open('stats\\processed_slmis.txt', "a")
    for m in stats_dates:
        # print(f"{spath}\\{m[0]}")
        # print(f"{m[0][:-30]} {m[1]}")
        subprocess.call(f'lua "lua\\src\\slmisconvert.lua" "{spath}\\{m[0]}" "{m[0][:-30]} {m[1]}"')
        processed_slmis.write(m[0] + "\n")
    processed_slmis.close()
    print("Finished Lua conversions")

    print("Scanning JSONs")
    mpath = "C:\\Users\\Walter\\Desktop\\DCStats Django\\DCStats-Project\\slmis\\"
    new_files = []
    for root, dirs, files in os.walk(mpath):
        for file in files:
            if file.endswith('.json'):
                new_files.append(file)
    

    pilot_list = get_pilots()
    exclude = []
    try:        
        with open('stats\\finishedfiles.txt', "r") as finishedfiles:
            for line in finishedfiles:
                exclude.append(line[:-1])
        finishedfiles.close()

    except FileNotFoundError:
        pass

    new_count = len(new_files)-len(exclude)

    print(f'Found {new_count} new files to import')

    for file in new_files:
        if file in exclude:
            pass
        else:
            date_str = file[-29:-5]
            filename = mpath + file
            stats_json = load_json(filename)
            if stats_json != []:
                for p in pilot_list:
                    try:
                        for k in stats_json[p]['times'].keys():
                            aircraft = k
                            in_air_sec = stats_json[p]['times'][k]['inAir']
                            total_sec = stats_json[p]['times'][k]['total']
                            pilot = Pilot.objects.get(clientid=p)
                            date = datetime.datetime.strptime(date_str, "%b %d, %Y at %H %M %S")
                            new_mission = Mission.manager.create_entry(aircraft, in_air_sec, total_sec, pilot, file[:-30], date)
                    except KeyError:
                        print(f'No entry for {p} in {file}')
                    except AttributeError:
                         print(f'No entry for {p} in {file}')
        
            with open('stats\\finishedfiles.txt', 'a') as finishedfiles:
                finishedfiles.write(file + '\n')
            finishedfiles.close()
            print(f'Imported {file}')


def delete_mission():
    aircraft = Mission.objects.all().delete()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--mission',
            action='store_true',
            dest='mission',
            help='Update slmod mission stats files only')
        parser.add_argument(
            '--deletemission',
            action='store_true', 
            dest='deletemission', 
            help='Deletes all records in Mission table')
    def handle(self, **options):
        if options['mission']:
            return mis_update()
        elif options['deletemission']:
            return delete_mission()
        else:
            return update_stats()
