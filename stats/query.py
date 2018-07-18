#dqueries
import datetime
from .models import *
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from django.db.models.functions import TruncDay

def filter_date(datefilter):
	if datefilter == 'all':
		date_filter = all_dates()

	elif datefilter == 'week':
		date_filter = last_week()

	elif datefilter == 'month':
		date_filter = last_month()

	elif datefilter == 'quarter':
		date_filter = last_quarter()

	return date_filter

def last_week():
	start_date = datetime.datetime.now() + datetime.timedelta(-7)
	return start_date

def all_dates():
	date_filter = datetime.datetime.now()
	date_filter = date_filter.replace(year=date_filter.year-50)
	return date_filter

def last_month():
	date_filter = datetime.datetime.now() + datetime.timedelta(-30)
	return date_filter

def last_quarter():
	date_filter = datetime.datetime.now() + datetime.timedelta(-90)
	return date_filter

def execute(options):
	print(f'in execute function {options}')
	groups = options['group_by']
	all_pilots = Pilot.objects.all()
	missions = Stats.objects.filter(mission__date__range=(options['start_date'], options['end_date']))
	if options['pilot_filter'] != 'All':
		missions = missions.filter(pilot=options['pilot_filter'])
	if options['aircraft_filter'] != 'All':
		missions = missions.filter(aircraft=options['aircraft_filter'])
		# pilot = Pilot.objects.get(clientid=clientid)
		# name = str(pilot)
		# rank = pilot.rank_id
	if  'day' in groups or '-day' in options['sort_by']:
		stats = missions \
			.annotate(day = TruncDay('mission__date')) \
			.values(*groups) \
			.annotate(in_air_hours=Sum('in_air_sec') / 3600,
		    hours_on_server=Sum('total_sec') / 3600,
		    losses=Sum('losses'), ground_kills=Sum('ground_kills'),
		    aircraft_kills=Sum('aircraft_kills'), ship_kills=Sum('ship_kills'),
		    landings=Sum('landings'), traps=Sum('traps'), aar=Sum('aar')) \
		    .order_by(options['sort_by'])

	else:
		stats = missions.values(*groups) \
		.annotate(in_air_hours=Sum('in_air_sec') / 3600,
		    hours_on_server=Sum('total_sec') / 3600,
		    losses=Sum('losses'), ground_kills=Sum('ground_kills'),
		    aircraft_kills=Sum('aircraft_kills'), ship_kills=Sum('ship_kills'),
		    landings=Sum('landings'), traps=Sum('traps'), aar=Sum('aar')) \
		    .order_by(options['sort_by'])

	if 'pilot' in groups:
		for s in stats:
			pobject = Pilot.objects.get(clientid=s['pilot'])
			name = str(pobject)
			rank = pobject.rank_id
			s['pilot'] = name
			s['rank'] = rank
	print(stats)
	return stats

def NewStats(user, get):
	stats = Stats.objects.filter(pilot=user, new=get['new_only'], mission__date__range=(get['start_date'], get['end_date']))
	return stats

# def execute(request, clientid, datefilter, **groups):
# 	groups = groups
# 	all_pilots = Pilot.objects.all()
# 	missions = Stats.objects.filter(date__gte=filter_date(datefilter))
# 	if clientid != 'all':
# 		missions = missions.filter(pilot=clientid)
# 		# pilot = Pilot.objects.get(clientid=clientid)
# 		# name = str(pilot)
# 		# rank = pilot.rank_id
# 	stats = missions.values(*groups.values()) \
# 	        .annotate(in_air_hours=Sum('in_air_sec') / 3600,
# 		    hours_on_server=Sum('total_sec') / 3600,
# 		    losses=Sum('crash'),
# 		    all_aircraft_kills=Sum('all_aircraft_kills'),
# 		    surface_kills=Sum('building_kills') + Sum('ground_kills') + Sum('ship_kills')) \
# 		    .order_by('-in_air_hours')
# 	if 'pilot' in groups.values():
# 		for s in stats:
# 			pobject = Pilot.objects.get(clientid=s['pilot'])
# 			name = str(pobject)
# 			rank = pobject.rank_id
# 			s['pilot'] = name
# 			s['rank'] = rank
# 	return render(request, 'stats/pilot_stats.html', {'stats':stats, 'pilots':all_pilots})
