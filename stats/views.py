'''
stats.views
'''
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from stats import query
from home.decorators import user_tz
from .models import Pilot, Stats
from .forms import StatsOptions, LogForm, LogFilter

@user_tz
@login_required
def pilot_stats(request):
    '''
    Displays the Leaderboard page

    **Context**
    ''form''
        An instance of forms.StatsOptions

    ''stats''
        dict from query.execute on :model:'stats.Stats'

    ''start_date''
        The currently selected start_date in form

    ''end_date''
        The currently selected end_date in form

    **Template**
        :template:'stats/leaderboard.html'
    '''
    try:
        user = request.user
        user = Pilot.objects.get(user=user)
        if request.method == 'POST':
            form = StatsOptions(request.POST)
            print(f'Request:  {request.POST}')
            if form.is_valid():
                options = form.cleaned_data
                stats = query.execute(options)
                print(f'OPTIONS:{options}')
                start_date = options['start_date']
                end_date = options['end_date']
                return render(request, 'stats/leaderboard.html',
                              {
                                  'form':form, 'stats':stats,
                                  'start_date':start_date.date, 'end_date':end_date.date
                              }
                             )
        else:
            start_date = timezone.localtime()
            start_date = query.last_week(start_date)
            end_date = timezone.localtime().replace(hour=0, minute=0, second=0)
            end_date = query.end_day(end_date)
            form = StatsOptions(initial={
                'group_by':['pilot__callsign'],
                'start_date':start_date.date(),
                'end_date':end_date.date()})
            options = {'group_by': ['pilot__callsign'],
                       'start_date': start_date,
                       'end_date': end_date,
                       'aircraft_filter': None,
                       'pilot_filter': None,
                      }
            print(options)
            stats = query.execute(options)

        return render(request,
                      'stats/leaderboard.html',
                      {
                          'form':form,
                          'stats':stats,
                          'start_date':start_date.date,
                          'end_date':end_date.date
                      }
                     )
    except ObjectDoesNotExist:
        return redirect('inactive')

@login_required
@user_tz
def log_entry(request):
    '''
    Displays an individual :model:'stats.Stats' for editing

    **Context**
    ''stat''
        An instance of :model:'stats.Stats'

    ''hours''
        Dict holding hours conversion from :model:'stats.Stats.in_air_sec'
        and :model:'stats.Stats.total_sec'

    ''logform''
        An instance of forms.LogForm

    **Template**
        :template:'stats/log_entry.html'
    '''
    if request.method == 'POST':
        stat = Stats.objects.get(pk=request.POST['statid'])
        logform = LogForm(request.POST, instance=stat)
        if logform.is_valid():
            stat = logform.save(commit=False)
            stat.new = 0
            stat.save()
    else:
        stat = Stats.objects.get(pk=request.GET['stat'])
        logform = LogForm(instance=stat)
        hours = {}
        hours['in_air'] = stat.in_air_sec / 3600
        hours['on_server'] = stat.total_sec / 3600
    return render(request,
                  f'stats/log_entry.html',
                  {
                      'stat':stat,
                      'hours':hours,
                      'logform':logform
                  }
                 )

@login_required
@user_tz
def pilot_log(request):
    '''
    Displays instances of :model:'stats.Stats' related to currently logged in user

    **Context**
    ''log_filter''
        An instance of forms.LogFilter

    ''logs''
        A queryset of :model:'stats.Stats' from query.new_stats

    **Template**
        :template:'stats/pilot_log.html'
    '''
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
    end_date = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = query.end_day(end_date)
    log_filter = LogFilter(initial={'start_date':start_date.date, 'end_date':end_date.date})
    options = {'new_only':1, 'start_date':start_date, 'end_date':end_date}
    logs = query.new_stats(pilot, options)
    return render(request, 'stats/pilot_log.html', {'log_filter':log_filter, 'logs':logs})
