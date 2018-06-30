from django.http import HttpResponse
from django.shortcuts import render
from .models import Pilot, Aircraft, PilotTotal, AircraftTotal, Mission
from stats.dqueries import *

def stats(request):
	pilots = Pilot.objects.all()
	totals = pilot_totals(pilots)
	return render(request, 'stats/stats.html', {'pilots':pilots, 'totals':totals,})

def pilot_stats(request):
	clientid = request.GET['clientid']
	pilots = Pilot.objects.all()

	if clientid == 'Pilot Totals':
		totals = pilot_totals(pilots)		
		return render(request, 'stats/stats.html', {'pilots':pilots, 'totals':totals,})
	
	else:
		a_models = Aircraft.objects.filter(pilot=clientid)
		aircraft = []
		for a in a_models:
			aircraft.append(aircraft_totals(a, clientid))
		return render(request, 'stats/pilot_stats.html',{'pilots':pilots, 'clientid':clientid, 'aircraft':aircraft})

	
