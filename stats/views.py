import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from .models import Pilot, Aircraft, Stats
from .forms import StatsOptions, LogForm, LogFilter
from stats import query
from home.views import inactive

def stats(request):
	clientid = 'all'
	pilots = ''
	aircraft = ''
	return render(request, 'stats/pilot_stats.html', {'pilots':pilots, 'clientid':clientid, 'aircraft':aircraft})

@login_required
def pilot_stats(request):
	try:
		start_date = datetime.date.today() - datetime.timedelta(days=7)
		end_date = datetime.date.today()
		log_filter=LogFilter()
		get = {'new_only':1, 'start_date':start_date, 'end_date':end_date}
		user = request.user
		user = Pilot.objects.get(user=user)
		new_stats = query.NewStats(user, get)

		if request.method == 'POST':
			if request.POST['query'] == 'True':
				form = StatsOptions(request.POST)
				log_filter = LogFilter()
				print(request.POST)
				if form.is_valid():
					options = form.cleaned_data
					stats = query.execute(options)
					groups = options['group_by']
					return render(request, 'stats/pilot_stats.html', {'form':form, 'log_filter':log_filter, 'stats':stats, 'new_stats':new_stats})
			else:
				log_filter = LogFilter(request.POST)
				if log_filter.is_valid():
					options = log_filter.cleaned_data
					new_stats = query.NewStats(user, options)
					print(request.POST)


		
		form = StatsOptions(initial={'group_by':['pilot','day',
									 'aircraft','mission__name'],
									 'sort_by':'-day',
									 'pilot_filter':user.clientid}
							)
		stats = query.execute({'group_by': ['pilot', 'aircraft',
			           'mission__name', 'day'],
			           'start_date': start_date,
			           'end_date': end_date,
			           'aircraft_filter': 'All',
			           'pilot_filter': user.clientid,
			           'sort_by': '-day'})
		
		# if request.GET:
		# 	get = request.GET
		# 	get['start_date'] = get['start_date_month'] + get['start_date_day'] + get['start_date_year=2018']
		# 	get['end_date'] = get['end_date_month'] + get['end_date_day'] + get['end_date_year=2018']
		# else:
		# 	start_date = datetime.date.today() - datetime.timedelta(days=7)
		# 	end_date = datetime.date.today()
				
	
	except ObjectDoesNotExist:
		print('INACTIVE')
		return redirect('inactive')
	return render(request, 'stats/pilot_stats.html', {'form':form, 'log_filter':log_filter, 'stats':stats, 'new_stats':new_stats})

@login_required
def log_entry(request):
	if request.method == 'POST':
		user = Pilot.objects.get(user=request.user)
		stat = Stats.objects.get(pk=request.POST['statid'])
		logform = LogForm(request.POST, instance=stat)
		print(logform)
		if logform.is_valid():
			stat = logform.save(commit=False)
			stat.new = 0
			stat.save()
		return redirect('stats')
	else:
		stat = Stats.objects.get(pk=request.GET['stat'])
		logform = LogForm(instance=stat)
	user = Pilot.objects.get(user=request.user)
	return render(request, f'stats/log_entry.html', {'stat':stat, 'logform':logform})

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
# 	return query.execute(request, clientid, datefilter, **groups)


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

	
