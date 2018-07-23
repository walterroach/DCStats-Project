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
		print(start_date)
		end_date = timezone.now()
		end_date = query.end_day(end_date)
		user = request.user
		user = Pilot.objects.get(user=user)

		if request.method == 'POST':
			form = StatsOptions(request.POST)
			if form.is_valid():
				options = form.cleaned_data
				stats = query.execute(options)
				print(options)
				return render(request, 'stats/leaderboard.html', {'form':form,'stats':stats})
		else:
			form = StatsOptions(initial={'group_by':['pilot']})
			options = {'group_by': ['pilot'],
			           'start_date': start_date,
			           'end_date': end_date,
			           'aircraft_filter': None,
			           'pilot_filter': None,
			           }
			print(options)
			stats = query.execute(options)	

			# {'group_by': ['pilot'],
			#  'start_date': datetime.datetime(2018, 7, 15, 0, 0, tzinfo=<DstTzInfo 'US/Central' CDT-1 day, 19:00:00 DST>), 
			#  'end_date': datetime.datetime(2018, 7, 22, 0, 0, tzinfo=<DstTzInfo 'US/Central' CDT-1 day, 19:00:00 DST>),
			#   'aircraft_filter': None, 
			#   'pilot_filter': None}
		return render(request, 'stats/leaderboard.html', {'form':form, 'stats':stats})
	except ObjectDoesNotExist:
		return redirect('inactive')
	

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
	else:
		stat = Stats.objects.get(pk=request.GET['stat'])
		logform = LogForm(instance=stat)
	user = Pilot.objects.get(user=request.user)
	hours = {}
	hours['in_air'] = stat.in_air_sec / 3600
	hours['on_server'] = stat.total_sec / 3600
	return render(request, f'stats/log_entry.html', {'stat':stat, 'hours':hours, 'logform':logform})	

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
	start_date = timezone.localtime()
	start_date = query.last_week(start_date)
	end_date = timezone.localtime().replace(hour=0, minute=0, second=0)
	end_date = query.end_day(end_date)
	log_filter = LogFilter()
	options = new_options = {'new_only':1, 'start_date':start_date, 'end_date':end_date}
	logs = query.new_stats(pilot, options)
		
	return render(request, 'stats/pilot_log.html', {'log_filter':log_filter, 'logs':logs})

