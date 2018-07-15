from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Pilot, Aircraft, Stats
from .forms import StatsOptions
from stats.query import *

def stats(request):
	clientid = 'all'
	pilots = ''
	aircraft = ''
	return render(request, 'stats/pilot_stats.html', {'pilots':pilots, 'clientid':clientid, 'aircraft':aircraft})

def pilot_stats(request):
	if request.method == 'POST':
		form = StatsOptions(request.POST)
		if form.is_valid():
			options = form.cleaned_data
			stats = execute(options)
			groups = options['group_by']
			return render(request, 'stats/pilot_stats.html', {'form':form, 'stats':stats, 'groups':groups})
	else:
		form = StatsOptions(initial={'group_by':'pilot', 'sort_by':'-in_air_hours'})

	return render(request, 'stats/pilot_stats.html', {'form':form})


# def pilot_stats(request):
# 	clientid = request.GET['clientid']
# 	datefilter = request.GET['date']
# 	group_by = request.GET['group_by']
# 	group_by2 = request.GET['group_by2']
# 	if group_by2 != '':
# 		groups = dict(
# 			group_by=group_by,
# 			group_by2=group_by2)
# 	else:
# 		groups = dict(group_by=group_by)
# 	return execute(request, clientid, datefilter, **groups)


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

	
