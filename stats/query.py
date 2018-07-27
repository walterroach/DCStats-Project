'''
stats.query
'''
import datetime
from django.db.models import Sum
from .models import Stats

def last_week(date):
    '''Take datetime object and return datetime object 7 days prior'''
    start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = start_date + datetime.timedelta(days=-7)
    return start_date

def end_day(date):
    '''Take datetime object and return datetime object with time set to 23 59 59 0'''
    end_date = date.replace(hour=23, minute=59, second=59, microsecond=0)
    return end_date

def execute(options):
    '''
    return dict of :models:'stats.Stats' queryset

    **arg**
    {
     'group_by':groups,
     'pilot_filter':clientid,
     'aircraft_filter':aircraft_id
     'start_date':datetime
     'end_date':datetime
     }
    '''
    groups = options['group_by']
    if 'pilot__callsign' in groups:
        groups.append('pilot__user__userprofile__rank_id__rank')
        groups.append('pilot__user__first_name')
        groups.append('pilot__user__last_name')
    if 'mission__name' in groups:
        groups.append('mission__date')
    missions = Stats.objects.filter(mission__date__range=(options['start_date'],
                                                          options['end_date']))
    if options['pilot_filter']:
        missions = missions.filter(pilot=options['pilot_filter'])
    if options['aircraft_filter']:
        missions = missions.filter(aircraft=options['aircraft_filter'])
    stats = missions.values(*groups) \
    .annotate(in_air_hours=Sum('in_air_sec') / 3600,
              hours_on_server=Sum('total_sec') / 3600,
              losses=Sum('losses'),
              ground_kills=Sum('ground_kills'),
              aircraft_kills=Sum('aircraft_kills'),
              ship_kills=Sum('ship_kills'),
              landings=Sum('landings'),
              traps=Sum('traps'),
              aar=Sum('aar')).order_by('-hours_on_server')
    return stats

def new_stats(user, options):
    '''
    Return queryset of :models:'stats.Stats', and related
    :models:'stats.Pilot' :models:'stats.aircraft' objects.

    **args**
    'user' as :models:'stats.Pilot' instance

    'options' as dict
        {'start_date':datetime, 'end_date':datetime}

    '''
    print(f"NEW STATS {options['start_date']}\n{options['end_date']}")
    stats = Stats.objects.filter(
        pilot=user,
        mission__date__range=(options['start_date'],
                              options['end_date'])) \
                         .annotate(
                             in_air_hours=Sum('in_air_sec') / 3600,
                             hours_on_server=Sum('total_sec') /3600) \
                         .order_by('-mission__date') \
                         .prefetch_related('pilot__user', 'pilot', 'mission', 'aircraft')
    return stats
