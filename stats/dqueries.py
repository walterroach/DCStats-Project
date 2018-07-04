#dqueries
from .models import *
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
import datetime

def pilot_totals(pilots):
	totals = []
	for pilot in pilots:
		x = PilotTotal(pilot.clientid)
		totals.append(x)
	
	for x in totals:
		print(x.name)
	return totals

def aircraft_totals(aircrafts):
	totals = []
	for aircraft in aircrafts:
		x = AircraftTotal(aircraft)
		totals.append(x)

	return totals

# def aircraft_totals(aircraft, clientid):
# 	a_missions = Mission.objects.filter(pilot=clientid, aircraft=aircraft)
# 	x = AircraftTotal(aircraft)
# 	print(clientid)
# 	for m in a_missions:
# 		x.add_mission(m)
# 	return x

class StatsRow:
	def __init__(self, name, rank, aircraft, in_air_hours, hours_on_server):
		self.name = name
		self.rank = rank
		self.aircraft = aircraft
		self.in_air_hours = in_air_hours
		self.hours_on_server = hours_on_server

	def __str__(self):
		return self.name

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

def group_by_pilot(request, all_pilots, clientid, datefilter):
	if clientid == 'all':
		pilots = all_pilots
	else:
		pilots = Pilot.objects.filter(clientid=clientid)

	date_filter = filter_date(datefilter)
	
	pilots = pilots.filter(mission__date__gte=date_filter).distinct()
	stats = [] 
	for pilot in pilots:
		m_filter = Mission.objects.filter(pilot=pilot, date__gte=date_filter)
		stats_query = m_filter.aggregate(in_air_hours=Sum('in_air_sec') / 3600, hours_on_server=Sum('total_sec') / 3600)
		new_row = StatsRow(str(pilot), pilot.rank_id, 'All', stats_query['in_air_hours'], stats_query['hours_on_server'])
		stats.append(new_row)
	stats.sort(key=lambda x: x.in_air_hours, reverse=True)
	return render(request, 'stats/pilot_stats.html', {'stats':stats, 'pilots':all_pilots})

class PilotPlaceholder:
			def __init__(self):
				rank_id = 'N/A'
				name = 'All'

			def __str__(self):
				return self.name

def group_by_aircraft(request, all_pilots, clientid, datefilter):
	if clientid == 'all':
		aircrafts = Aircraft.objects.all()
		pilot_filter = Mission.objects.all()
		pilot = PilotPlaceholder()
	else:
		aircrafts = Aircraft.objects.filter(mission__pilot=clientid)
		pilot_filter = Mission.objects.filter(pilot=clientid)
		pilot = Pilot.objects.get(clientid=clientid)
	date_filter = filter_date(datefilter)
	aircrafts = aircrafts.filter(mission__date__gte=date_filter).distinct()
	stats = []
	for aircraft in aircrafts:
		m_filter = pilot_filter.filter(aircraft=aircraft, date__gte=date_filter)
		stats_query = m_filter.aggregate(in_air_hours=Sum('in_air_sec') / 3600, hours_on_server=Sum('total_sec') / 3600)
		new_row = StatsRow(str(pilot), pilot.rank_id, aircraft.aircraft, stats_query['in_air_hours'], stats_query['hours_on_server'])
		# except UnboundLocalError:
		# 	new_row = StatsRow('All', 'N/A', aircraft.aircraft, stats_query['in_air_hours'], stats_query['hours_on_server'])
		stats.append(new_row)
	stats.sort(key=lambda x: x.in_air_hours, reverse=True)
	return render(request, 'stats/pilot_stats.html', {'stats':stats, 'pilots':all_pilots})

def group_by_pilot_aircraft(request, all_pilots, clientid, datefilter):
	if clientid == 'all':
		pilots = all_pilots
		print(f'all_pilots: {all_pilots}')
		print("clientid is all")
	else:
		pilots = Pilot.objects.filter(clientid=clientid)

	aircrafts = Aircraft.objects.all()
	print("aircraft query set to all")
	date_filter = filter_date(datefilter)
	aircrafts = aircrafts.filter(mission__date__gte=date_filter).distinct()
	print("aircraft filtered by date")
	pilots = pilots.filter(mission__date__gte=date_filter).distinct()
	stats = [] 
	for pilot in pilots:
		# aircrafts = aircrafts.filter(mission__pilot=pilot.clientid)
		# print("aircraft filtered by pilot")
		for aircraft in aircrafts:
			m_filter = Mission.objects.filter(pilot=pilot, aircraft=aircraft, date__gte=date_filter)
			stats_query = m_filter.aggregate(in_air_hours=Sum('in_air_sec') / 3600, hours_on_server=Sum('total_sec') / 3600)
			new_row = StatsRow(str(pilot), pilot.rank_id, aircraft.aircraft, stats_query['in_air_hours'], stats_query['hours_on_server'])
			if new_row.hours_on_server != None:
				print(f'Hours {new_row.hours_on_server}')
				stats.append(new_row)
	stats.sort(key=lambda x: (x.name, x.in_air_hours), reverse=True)
	return render(request, 'stats/pilot_stats.html', {'stats':stats, 'pilots':all_pilots})

def group_by_aircraft_pilot(request, all_pilots, clientid, datefilter):
	if clientid == 'all':
		pilots = all_pilots
		print(f'all_pilots: {all_pilots}')
		print("clientid is all")
	else:
		pilots = Pilot.objects.filter(clientid=clientid)

	aircrafts = Aircraft.objects.all()
	print("aircraft query set to all")
	date_filter = filter_date(datefilter)
	aircrafts = aircrafts.filter(mission__date__gte=date_filter).distinct()
	print("aircraft filtered by date")
	pilots = pilots.filter(mission__date__gte=date_filter).distinct()
	stats = [] 
	for pilot in pilots:
		# aircrafts = aircrafts.filter(mission__pilot=pilot.clientid)
		# print("aircraft filtered by pilot")
		for aircraft in aircrafts:
			m_filter = Mission.objects.filter(pilot=pilot, aircraft=aircraft, date__gte=date_filter)
			stats_query = m_filter.aggregate(in_air_hours=Sum('in_air_sec') / 3600, hours_on_server=Sum('total_sec') / 3600)
			new_row = StatsRow(str(pilot), pilot.rank_id, aircraft.aircraft, stats_query['in_air_hours'], stats_query['hours_on_server'])
			if new_row.hours_on_server != None:
				print(f'Hours {new_row.hours_on_server}')
				stats.append(new_row)
	stats.sort(key=lambda x: (x.aircraft, x.in_air_hours), reverse=True)
	return render(request, 'stats/pilot_stats.html', {'stats':stats, 'pilots':all_pilots})

class Dquery:
	def __init__(self):
		self.clientid = ''
		self.group_by = ''
		self.request = ''

	def execute(self, request, clientid, datefilter, group_by, group_by2):
		all_pilots = Pilot.objects.all()
		if group_by == 'pilot':
			if group_by2 == 'None':
				return group_by_pilot(request, all_pilots, clientid, datefilter,)
			elif group_by2 == 'aircraft':
				return group_by_pilot_aircraft(request, all_pilots, clientid, datefilter)
			else:
				return bad_request(group_by, group_by2)

		elif group_by == 'aircraft':
			if group_by2 == 'None':
				return group_by_aircraft(request, all_pilots, clientid, datefilter)
			elif group_by2 == 'pilot':
				return group_by_aircraft_pilot(request, all_pilots, clientid, datefilter)

	
			

	# def execute(self, request, clientid, group_by):
	# 	self.clientid = clientid
	# 	self.group_by = group_by
	# 	self.request = request

	# 	if self.clientid == 'all' and group_by == 'pilot':
	# 		return self.group_by_pilot(request)
	# 	elif group_by == 'pilot':
	# 		return self.group_by_pilot(request, self.clientid)
	# 	elif clientid == 'all' and group_by == 'aircraft':
	# 		return self.group_by_aircraft(request, )
	# 	else:
	# 		return self.group_by_aircraft(request, self.clientid)

	# def group_by_pilot(self, request, clientid=""):
	# 	if clientid == "":
	# 		pilots = Pilot.objects.all()	
	# 	else:
	# 		pilots = Pilot.objects.filter(clientid=clientid)
	# 	aircraft = pilot_totals(pilots)	
	# 	return render(request, 'stats/pilot_stats.html', {'pilots':pilots, 'clientid':clientid, 'aircraft':aircraft})

	# def group_by_aircraft(self, request, clientid=""):
	# 	pilots = []
	# 	if clientid == "":
	# 		aircrafts = Aircraft.objects.all()
	# 	else:
	# 		aircrafts = Aircraft.objects.filter(mission__pilot_id=clientid)
	# 	aircraft = aircraft_totals(aircrafts)

	# 	return render(request, 'stats/pilot_stats.html',{'pilots':pilots, 'clientid':clientid, 'aircraft':aircraft})

# class GetStats(Dquery): 

	# if clientid == 'all' and group_by == 'pilot':
	# 	pilots = Pilot.objects.all()
	# 	aircraft = pilot_totals(pilots)		
	# 	return render(request, 'stats/pilot_stats.html', {'pilots':pilots, 'clientid':clientid, 'aircraft':aircraft})
	
	# elif group_by == 'pilot':
	# 	pilots = Pilot.objects.filter(clientid=clientid)
	# 	aircraft = pilot_totals(pilots)
	# 	return render(request, 'stats/pilot_stats.html', {'pilots':pilots, 'clientid':clientid, 'aircraft':aircraft})

	# elif clientid == 'all' and group_by == 'aircraft':
	# 	pilots = Pilot.objects.all()
	# 	aircraft = []
	# 	for p in pilots:
	# 		a_models = Aircraft.objects.filter(pilot=p.clientid)
	# 		for a in a_models:
	# 			aircraft.append(aircraft_totals(a, p.clientid))
	# 	return render(request, 'stats/pilot_stats.html',{'pilots':pilots, 'clientid':clientid, 'aircraft':aircraft})

	# else:
	# 	pilots = Pilot.objects.filter(clientid=clientid)
	# 	a_models = Aircraft.objects.filter(pilot=clientid)
	# 	aircraft = []
	# 	for a in a_models:
	# 		aircraft.append(aircraft_totals(a, clientid))
	# 	return render(request, 'stats/pilot_stats.html',{'pilots':pilots, 'clientid':clientid, 'aircraft':aircraft})