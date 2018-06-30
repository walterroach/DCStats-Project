#dqueries
from .models import *

def pilot_totals(pilots):
	totals = []
	for pilot in pilots:
		x = PilotTotal(pilot.clientid)
		totals.append(x)
	
	for x in totals:
		print(x.name)
	return totals

def aircraft_totals(aircraft, clientid):
	a_missions = Mission.objects.filter(pilot=clientid, aircraft=aircraft)
	x = AircraftTotal(aircraft)
	for m in a_missions:
		x.add_mission(m)
	return x