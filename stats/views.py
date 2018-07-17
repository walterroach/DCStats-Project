from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .models import Pilot, Aircraft, Stats
from .forms import StatsOptions
from stats.query import *

def stats(request):
	clientid = 'all'
	pilots = ''
	aircraft = ''
	return render(request, 'stats/pilot_stats.html', {'pilots':pilots, 'clientid':clientid, 'aircraft':aircraft})

@login_required
def pilot_stats(request):
	LogEntrySet = modelformset_factory(Stats, fields=('all_aircraft_kills', 'death'))
	if request.method == 'POST':
		form = StatsOptions(request.POST)
		if form.is_valid():
			options = form.cleaned_data
			stats = execute(options)
			groups = options['group_by']
			return render(request, 'stats/pilot_stats.html', {'form':form, 'stats':stats, 'groups':groups})
	else:
		user = request.user
		user = Pilot.objects.get(user=user)
		start_date = datetime.date.today() - datetime.timedelta(days=7)
		end_date = datetime.date.today()
		user_stats = Stats.objects.filter(pilot=user)
		form = StatsOptions(initial={'group_by':['pilot','day',
									 'aircraft','mission__name'],
									 'sort_by':'-day',
									 'pilot_filter':user.clientid}
							)
		stats = execute({'group_by': ['pilot', 'aircraft',
			           'mission__name', 'day'],
			           'start_date': start_date,
			           'end_date': end_date,
			           'aircraft_filter': 'All',
			           'pilot_filter': user.clientid,
			           'sort_by': '-day'})

		new_stats = NewStats(user)
	return render(request, 'stats/pilot_stats.html', {'form':form, 'stats':stats, 'new_stats':new_stats})


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

	
