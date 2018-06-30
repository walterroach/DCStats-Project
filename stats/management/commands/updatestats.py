'''Updates Aircraft SQL table with data from most current slmod json.  Takes no arguments'''
import os
import json
import glob
import datetime
import pytz
import subprocess
from pathlib import Path
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
    dir_path = Path("/slmod/")
    list_of_files = glob.glob(dir_path)
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

def list_files(spath):
    mis_stats = []
    for root, dirs, files in os.walk(spath):
        for file in files:
            if file != 'SlmodMetaStats.lua' and file != 'SlmodStats.lua':
                mis_stats.append(file)
    return mis_stats

def update_mismodel(k, p, file, stats_json, date):
    aircraft = k
    in_air_sec = stats_json[p]['times'][k]['inAir']
    total_sec = stats_json[p]['times'][k]['total']
    pilot = Pilot.objects.get(clientid=p)
    new_mission = Mission.manager.create_entry(aircraft, in_air_sec, total_sec, pilot, file[:-30], date)

def mis_update():
    '''
    Updates Mission Django model from json
    '''
    print("Scanning stats folder")
    #Check for already converted slmod mission luas
    mpath = Path('D:/DCS/Willshouse/stats')
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
    for m in mis_stats:
        if m in exclude:
            pass
        else:
            subprocess.call(f'lua {slmis_lua} "{mpath}\\{m}" "{m[:-4]}"')
            processed_slmis.write(m + "\n")
    processed_slmis.close()
    print("Finished Lua conversions")
    #Check for already imported slmod mission JSONs
    print("Scanning JSONs")
    spath = Path("slmis")
    new_files = list_files(spath)
    pilot_list = get_pilots()
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
    for file in new_files:
        if file in exclude:
            pass
        else:
            lua_suff = file[:-5] + ".lua"
            lua_name = mpath / lua_suff
            date = datetime.datetime.fromtimestamp(os.path.getmtime(lua_name), pytz.UTC)
            filename = spath / file
            stats_json = load_json(filename)
            if stats_json != []:
                for p in pilot_list:
                    try:
                        for k in stats_json[p]['times'].keys():
                            update_mismodel(k, p, file, stats_json, date)
                    except KeyError:
                        pass
                    except AttributeError:
                        pass
            with open(finishedpath, 'a') as finishedfiles:
                finishedfiles.write(file + '\n')
            finishedfiles.close()
    print("Finished Import with no errors")


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
