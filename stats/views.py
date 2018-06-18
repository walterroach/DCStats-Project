from django.http import HttpResponse
from django.shortcuts import render
from .models import Pilot
from .models import Slmod_Total
import json

def stats(request):
	pilots = Pilot.objects
	stats = Slmod_Total.objects
	return render(request, 'stats/stats.html', {'pilots':pilots},
	 {'stats':stats})

def pilot_stats(request):
	clientid = request.GET['clientid']

	return render(request, 'stats/stats.html',{'clientid':clientid,})

def search_client(request):
	stats = Slmod_Total.objects
	stats.file
	fulltext = request.GET('fulltext')
	
