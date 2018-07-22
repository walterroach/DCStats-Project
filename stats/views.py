import datetime
from django.utils import timezone
import pytz
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from .models import Pilot, Aircraft, Stats
from .forms import StatsOptions, LogForm, LogFilter
from stats import query
from home.views import inactive
from home.decorators import user_tz


def stats(request):
	clientid = 'all'
	pilots = ''
	aircraft = ''
	return render(request, 'stats/pilot_stats.html', {'pilots':pilots, 'clientid':clientid, 'aircraft':aircraft})

@login_required
def pilot_stats(request):
	try:
		start_date =timezone.now()
		start_date = query.last_week(start_date)
		end_date = timezone.now()
		end_date = query.end_day(end_date)
		log_filter=LogFilter()
		new_options = {'new_only':1, 'start_date':start_date, 'end_date':end_date}
		user = request.user
		user = Pilot.objects.get(user=user)
		new_stats = query.new_stats(user, new_options)

		if request.method == 'POST':
			if request.POST['query'] == 'True':
				form = StatsOptions(request.POST)
				log_filter = LogFilter()
				if form.is_valid():
					options = form.cleaned_data
					stats = query.execute(options)
					groups = options['group_by']
					return render(request, 'stats/pilot_stats.html', {'form':form, 'log_filter':log_filter, 'stats':stats, 'new_stats':new_stats})
			else:
				log_filter = LogFilter(request.POST)
				if log_filter.is_valid():
					options = log_filter.cleaned_data
					new_stats = query.new_stats(user, options)


		
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
	except ObjectDoesNotExist:
		return redirect('inactive')
	return render(request, 'stats/pilot_stats.html', {'form':form, 'log_filter':log_filter, 'stats':stats, 'new_stats':new_stats})

@login_required
@user_tz
def log_entry(request):
	if request.method == 'POST':
		user = Pilot.objects.get(user=request.user)
		stat = Stats.objects.get(pk=request.POST['statid'])
		logform = LogForm(request.POST, instance=stat)
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

@login_required
@user_tz
def pilot_log(request):
	#checks if user active
	try:
		pilot = Pilot.objects.get(user=request.user)
	except ObjectDoesNotExist:
		return redirect('inactive')
	if request.method == 'POST':
		log_filter = LogFilter(request.POST)
		if log_filter.is_valid():
			clean = log_filter.cleaned_data
			# clean['start_date'] = log_filter.
			logs = query.new_stats(pilot, clean)
			return render(request, 'stats/pilot_log.html', {'log_filter':log_filter, 'logs':logs})
	start_date = timezone.localtime() + datetime.timedelta(-7)
	start_date = query.last_week(start_date)
	end_date = timezone.localtime().replace(hour=0, minute=0, second=0)
	end_date = query.end_day(end_date)
	log_filter = LogFilter()
	options = new_options = {'new_only':1, 'start_date':start_date, 'end_date':end_date}
	logs = query.new_stats(pilot, options)
		
	return render(request, 'stats/pilot_log.html', {'log_filter':log_filter, 'logs':logs})

