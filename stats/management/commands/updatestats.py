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

def list_files(spath):
    mis_stats = []
    for root, dirs, files in os.walk(spath):
        for file in files:
            if file != 'SlmodMetaStats.lua' and file != 'SlmodStats.lua':
                mis_stats.append(file)
    return mis_stats

def update_mismodel(aircrafts, pilots, file, stats_json, date):
    in_air_sec = stats_json[pilots]['times'][aircrafts.aircraft]['inAir']
    total_sec = stats_json[pilots]['times'][aircrafts.aircraft]['total']
    pilot = Pilot.objects.get(clientid=pilots)
    new_mission = Mission.manager.create_entry(aircrafts, 
                                                in_air_sec,
                                                total_sec, 
                                                pilot, 
                                                file[:-30],
                                                date)

def mis_update():
    '''
    Updates Mission Django model from json
    '''
    print("Scanning stats folder")
    #Check for already converted slmod mission luas
    mpath = Path('slmod/')
    mis_stats = list_files(mpath)
    print(f'mis_stats after list_files() = {mis_stats}')
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
            mpath_m = str(mpath) +"/"+ m
            process = f'lua {slmis_lua} "{mpath}/{m}" "/{m[:-4]}"'
            print(process)
            subprocess.call(process, shell=True)
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
    progress = 0
    for file in new_files:
        if file in exclude:
            pass
        else:
            progress += 1
            print(f'Importing {progress} of {new_count}')
            lua_suff = file[:-5] + ".lua"
            lua_name = mpath / lua_suff
            date = datetime.datetime.fromtimestamp(os.path.getmtime(lua_name), pytz.UTC)
            filename = spath / file
            stats_json = load_json(filename)
            if stats_json != []:
                for p in pilot_list:
                    try:
                        for k in stats_json[p]['times'].keys():
                            new_aircraft = Aircraft.objects.get_or_create(aircraft=k)
                            new_aircraft = Aircraft.objects.get(aircraft=k)                    
                            update_mismodel(new_aircraft, p, file, stats_json, date)
                    except KeyError as e:
                        pass
                    except AttributeError as e:
                        pass
            with open(finishedpath, 'a') as finishedfiles:
                finishedfiles.write(file + '\n')
            finishedfiles.close()
    print("Finished Import with no errors")


def delete_mission():
    aircraft = Mission.objects.all().delete()

def delete_aircraft():
    aircraft = Aircraft.objects.all().delete()

def list_aircraft():
    aircrafts = Aircraft.objects.all()

class Command(BaseCommand):
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
            return delete_mission()
        elif options['deleteaircraft']:
            return delete_aircraft()
        elif options['list_aircraft']:
            return list_aircraft()
        else:
            return mis_update()
