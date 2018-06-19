from django.http import HttpResponse
from django.shortcuts import render
from .models import Pilot
from .models import Aircraft
from stats import dqueries


def stats(request):
	pilots = Pilot.objects.all()
	totals = []
	for pilot in pilots:
		x = dqueries.PilotTotal(pilot.clientid)
		totals.append(x)
	
	for x in totals:
		print(x.name)
	
	return render(request, 'stats/stats.html', {'pilots':pilots, 'totals':totals,})

def pilot_stats(request):
	clientid = request.GET['clientid']

	return render(request, 'stats/stats.html',{'clientid':clientid,})

def search_client(request):
	stats = Slmod_Total.objects
	stats.file
	fulltext = request.GET('fulltext')
	
