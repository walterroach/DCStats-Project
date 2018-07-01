#dqueries
from .models import *
from django.shortcuts import render
from django.http import HttpResponse

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

class Dquery:
	def __init__(self):
		self.clientid = ''
		self.group_by = ''
		self.request = ''

	def execute(self, request, clientid, group_by):
		self.clientid = clientid
		self.group_by = group_by
		self.request = request

		if self.clientid == 'all' and group_by == 'pilot':
			return self.group_by_pilot(request)
		elif group_by == 'pilot':
			return self.group_by_pilot(request, self.clientid)
		elif clientid == 'all' and group_by == 'aircraft':
			return self.group_by_aircraft(request, )
		else:
			return self.group_by_aircraft(request, self.clientid)

	def group_by_pilot(self, request, clientid=""):
		if clientid == "":
			pilots = Pilot.objects.all()	
		else:
			pilots = Pilot.objects.filter(clientid=clientid)
		aircraft = pilot_totals(pilots)	
		return render(request, 'stats/pilot_stats.html', {'pilots':pilots, 'clientid':clientid, 'aircraft':aircraft})

	def group_by_aircraft(self, request, clientid=""):
		pilots = []
		if clientid == "":
			aircrafts = Aircraft.objects.all()
		else:
			aircrafts = Aircraft.objects.filter(mission__pilot_id=clientid)
		aircraft = aircraft_totals(aircrafts)

		return render(request, 'stats/pilot_stats.html',{'pilots':pilots, 'clientid':clientid, 'aircraft':aircraft})

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