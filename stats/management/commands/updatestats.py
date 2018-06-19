from django.core.management.base import BaseCommand, CommandError
from stats import models
from stats.models import Pilot, Total, Aircraft, AircraftManager
import os
import json
import glob

def getdir():
	try:
		dir_path = os.getcwd() + '\\slmod'
	except:
		dir_path = os.getcwd() +'/slmod'

	list_of_files = glob.glob(dir_path + '\\*')
	latest_file = max(list_of_files, key=os.path.getctime)
	
	return fetch_stats(latest_file)

def fetch_stats(fpath):
	stats_file = open(fpath)
	stats_json = stats_file.read()
	stats_json = json.loads(stats_json)
	stats_file.close()

	return get_clientids(stats_json)

def get_clientids(stats_json):
	pilots = Pilot.objects.all()
	pilot_list = []
	for pilot in pilots:
		pilot_list.append(pilot.clientid)
	print(pilot_list)
	return update_model(stats_json, pilot_list)

def update_model(stats_json, pilot_list):
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

	return 'done'


class Command(BaseCommand):
	def handle(self, **options):
		return getdir()

	#totals = Total.objects.all()
	#for pilot in totals:
	#	pilot.
