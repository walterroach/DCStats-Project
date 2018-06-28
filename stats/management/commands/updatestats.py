'''Updates Aircraft SQL table with data from most current slmod json.  Takes no arguments'''
import os
import json
import glob
import datetime
import subprocess
from django.core.management.base import BaseCommand, CommandError
from stats.models import Pilot, Aircraft


def update_stats():
    '''Updates Aircraft SQL table with data from most current slmod json'''
    #Clear exsiting aircraft database.
    aircraft = Aircraft.objects.all().delete()

    #Finds and loads most recent stats_YYYY_MM_DD_TTTT.json file
    try:
        dir_path = os.getcwd() + '\\slmod'
    except:
        dir_path = os.getcwd() +'/slmod'

    list_of_files = glob.glob(dir_path + '\\*')
    fpath = max(list_of_files, key=os.path.getctime)
    stats_file = open(fpath)
    stats_json = stats_file.read()
    stats_json = json.loads(stats_json)
    stats_file.close()

    #Fetches current active users from Pilot SQL table
    pilots = Pilot.objects.all()
    pilot_list = []
    for pilot in pilots:
        pilot_list.append(pilot.clientid)

    #Updates aircraft database with new data
    for p in pilot_list:
        for k in stats_json[p]['times'].keys():
            try:
                aircraft = k
                in_air_sec = stats_json[p]['times'][k]['inAir']
                total_sec = stats_json[p]['times'][k]['total']
                pilot = Pilot.objects.get(clientid=p)
                new_aircraft = Aircraft.manager.create_aircraft(aircraft,
                                                                in_air_sec, total_sec, pilot)
            except:
                break

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
    for m in mis_stats:
        date_str = m[-28:-16]
        date = datetime.datetime.strptime(date_str, '%b %d, %Y')
        date = date.date()
        s_d = (m,date)
        stats_dates.append(s_d)
    print(f'Found {len(stats_dates)} SlMod Mission Files')
    print(stats_dates)
    print("Converting SlMod mission files to JSON")
    for m in stats_dates:
        subprocess.call(f'lua "lua\\src\\slmisconvert.lua" "{spath}\\{m[0]}" "{m[0][:-30]} {m[1]}"')




class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--mission',
            action='store_true',
            dest='mission',
            help='Update slmod mission stats files only')

    def handle(self, **options):
        if options['mission']:
            return mis_update()
        else:
            return update_stats()
