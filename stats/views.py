from django.http import HttpResponse
from django.shortcuts import render
from .models import Pilot, Aircraft, PilotTotal, AircraftTotal
from .models import Aircraft



def stats(request):
	pilots = Pilot.objects.all()
	totals = []
	for pilot in pilots:
		x = PilotTotal(pilot.clientid)
		totals.append(x)
	
	for x in totals:
		print(x.name)
	
	return render(request, 'stats/stats.html', {'pilots':pilots, 'totals':totals,})

def pilot_stats(request):
	clientid = request.GET['clientid']
	pilots = Pilot.objects.all()

	if clientid == 'Pilot Totals':
		totals = []
		for pilot in pilots:
			x = PilotTotal(pilot.clientid)
			totals.append(x)
		
		for x in totals:
			print(x.name)
		
		return render(request, 'stats/stats.html', {'pilots':pilots, 'totals':totals,})
	
	else:
		acmodels = Aircraft.objects.filter(pilot=clientid)
		aircraft = []
		for a in acmodels:
			print(a)
			x = AircraftTotal(a)
			aircraft.append(x)
			print(aircraft)
		return render(request, 'stats/pilot_stats.html',{'pilots':pilots, 'clientid':clientid, 'aircraft':aircraft})

	
