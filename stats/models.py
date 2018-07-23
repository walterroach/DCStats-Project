
'''
Django models for stats app
'''
from django.db import models
from django.contrib.auth.models import User
import django.utils
import datetime
import pytz

class Pilot(models.Model):
    '''
    Django model class Pilot SQL table.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    clientid = models.CharField(max_length=32,
                                primary_key=True)
    callsign = models.CharField(max_length=30)
    rank_id = models.ForeignKey('Rank', null=True, blank=True,
                                on_delete=models.SET_NULL,
                                default=7)
    tz_choices = list()
    for tz in pytz.common_timezones:
        tz_choices.append((tz, tz))
    tz_choices = tuple(tz_choices)
    timezone = models.CharField(max_length=30, default='UTC', choices=tz_choices)

    def __str__(self):
        '''Return string value of Pilot'''
        try:
            name = f'{self.user.first_name} "{self.callsign}" {self.user.last_name}'
        except AttributeError:
            name = f'"{self.callsign}"'

        return name

    # def stats(self, clientid):
    #     self.air_hours = int

class Rank(models.Model):
    '''
    Django model class Rank SQL table.
    '''
    rank_choices = (
        ("O1", "O-1"),
        ("O2", "O-2"),
        ("O3", "O-3"),
        ("O4", "O-4"),
        ("O5", "O-5"),
        ("O6", "O-6"),
        ("Guest", "Guest")
        )
    rank = models.CharField(max_length=5,
                            choices=rank_choices)
    AF_name = models.CharField(max_length=30)
    Navy_name = models.CharField(max_length=30)

    def __str__(self):
        return self.rank


class AircraftManager(models.Manager):
    '''
    Django Manager class for editing Aircraft SQL table.
    '''
    def create_entry(self, aircraft):
        '''
        Create a record in Aircraft SQL database and return it.
        '''
        #checks for existing entry
        
        new_aircraft = self.create(aircraft=aircraft)
        return new_aircraft

# class StatsManager(models.Manager):
#     '''
#     Django Manager class for editing Aircraft SQL table.
#     '''
#     def create_entry(self, aircraft, in_air_sec, total_sec, pilot, missions, date,
#                      crash, eject, death, friendly_col_hits, friendly_col_kills,
#                      friendly_hits, friendly_kills, building_kills, ground_kills,
#                      heli_kills, fighter_kills, all_aircraft_kills, ship_kills, ip_flag, file):
#         '''
#         Create a record in Stats SQL database and return it.
#         '''
#         print(f'From models {ip_flag}')
#         # try:
#         print('MODELS')
#         mission = Stats.objects.get_or_create(aircraft=aircraft, pilot=pilot, file=file)
#         mission = mission[0]
#         mission.in_air_sec=in_air_sec
#         mission.total_sec=total_sec
#         mission.mission=missions
#         mission.date=date
#         # mission.crash=crash
#         # mission.eject=eject
#         # mission.death=death
#         # mission.friendly_col_hits=friendly_col_hits
#         # mission.friendly_col_kills=friendly_col_kills
#         # mission.friendly_hits=friendly_hits
#         # mission.friendly_kills=friendly_kills
#         # mission.building_kills=building_kills
#         # mission.ground_kills=ground_kills
#         # mission.heli_kills=heli_kills
#         # mission.fighter_kills=fighter_kills
#         # mission.all_aircraft_kills=all_aircraft_kills
#         # mission.ship_kills=ship_kills
#         mission.ip_flag=ip_flag
#         mission.file=file
#         mission.save()
#         # .save(update_fieldsaircraft=aircraft, 
#                     # in_air_sec=in_air_sec,
#                     # total_sec=total_sec,
#                     # pilot=pilot,
#                     # mission=mission,
#                     # date=date,
#                     # crash=crash,
#                     # eject=eject,
#                     # death=death,
#                     # friendly_col_hits=friendly_col_hits,
#                     # friendly_col_kills=friendly_col_kills,
#                     # friendly_hits=friendly_hits,
#                     # friendly_kills=friendly_kills,
#                     # building_kills=building_kills,
#                     # ground_kills=ground_kills,
#                     # heli_kills=heli_kills,
#                     # fighter_kills=fighter_kills,
#                     # all_aircraft_kills=all_aircraft_kills,
#                     # ship_kills=ship_kills,
#                     # ip_flag=ip_flag,
#                     # file=file)
                    
#         # mission.save()
#         # except:
#         #     print('EXCEPTING!')
#         #     mission = self.create(aircraft=aircraft, in_air_sec=in_air_sec,
#         #                       total_sec=total_sec, pilot=pilot, mission=mission, date=date,
#         #                       crash=crash, eject=eject, death=death, friendly_col_hits=friendly_col_hits,
#         #                       friendly_col_kills=friendly_col_kills, friendly_hits=friendly_hits,
#         #                       friendly_kills=friendly_kills, building_kills=building_kills,
#         #                       ground_kills=ground_kills, heli_kills=heli_kills, fighter_kills=fighter_kills,
#         #                       all_aircraft_kills=all_aircraft_kills, ship_kills=ship_kills, ip_flag=ip_flag, file=file)
        

class Aircraft(models.Model):
    '''
    Django Model class Aircraft SQL table
    '''
    aircraft = models.CharField(max_length=30, primary_key=(True))
    objects = models.Manager()
    manager = AircraftManager()

    def __str__(self):
        return f"{self.aircraft}"

class Mission(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=False,
                     auto_now=False, null=True, blank=True)
    file = models.CharField(max_length=250)
    in_process = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return(f'{self.name} {self.date}')

class Stats(models.Model):
    '''
    Django Model class Stats SQL table.  
    Contains data from slmod mission files.  
    '''
    aircraft = models.ForeignKey(Aircraft,
                                on_delete=models.CASCADE)
    in_air_sec = models.FloatField(default=0)
    total_sec = models.FloatField(default=0)
    pilot = models.ForeignKey(Pilot,
                              on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission,
                                on_delete=models.CASCADE)
    # manager = StatsManager()
    objects = models.Manager()
    losses = models.IntegerField(default=0)
    ground_kills = models.IntegerField(default=0)
    aircraft_kills = models.IntegerField(default=0)
    ship_kills = models.IntegerField(default=0)
    landings = models.IntegerField(default=0)
    traps = models.IntegerField(default=0)
    aar = models.IntegerField(default=0)
    new = models.IntegerField(default=1)
    

    def __str__(self):
        return f"{self.mission.date.strftime('%m/%d/%y %H:%MZ')} \
                 {self.aircraft} {self.pilot}"

# class UserStats(models.Model):
#     stats = models.ForeignKey(Stats,
#                               on_delete=models.CASCADE)
#     losses = models.IntegerField(default=0)
#     aircraft_kills = models.IntegerField(default=0)