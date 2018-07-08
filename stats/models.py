
'''
Django models for stats app
'''
from django.db import models
import django.utils
import datetime

class Pilot(models.Model):
    '''
    Django model class Pilot SQL table.
    '''
    clientid = models.CharField(max_length=32,
                                primary_key=True)
    f_name = models.CharField(max_length=30,
                              default='')
    l_name = models.CharField(max_length=30,
                              default='')
    callsign = models.CharField(max_length=30)
    rank_id = models.ForeignKey('Rank', null=True,
                                on_delete=models.SET_NULL,
                                default=7)

    def __str__(self):
        '''Return string value of Pilot'''
        return f'{self.f_name} "{self.callsign}" {self.l_name}'

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

class MissionManager(models.Manager):
    '''
    Django Manager class for editing Aircraft SQL table.
    '''
    def create_entry(self, aircraft, in_air_sec, total_sec, pilot, mission, date,
                     crash, eject, death, friendly_col_hits, friendly_col_kills,
                     friendly_hits, friendly_kills, building_kills, ground_kills,
                     heli_kills, fighter_kills, all_aircraft_kills, ship_kills):
        '''
        Create a record in Mission SQL database and return it.
        '''
        mission = self.create(aircraft=aircraft, in_air_sec=in_air_sec,
                              total_sec=total_sec, pilot=pilot, mission=mission, date=date,
                              crash=crash, eject=eject, death=death, friendly_col_hits=friendly_col_hits,
                              friendly_col_kills=friendly_col_kills, friendly_hits=friendly_hits,
                              friendly_kills=friendly_kills, building_kills=building_kills,
                              ground_kills=ground_kills, heli_kills=heli_kills, fighter_kills=fighter_kills,
                              all_aircraft_kills=all_aircraft_kills, ship_kills=ship_kills)
        return mission

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
    '''
    Django Model class Mission SQL table.  
    Contains data from slmod mission files.  
    '''
    aircraft = models.ForeignKey(Aircraft,
                                on_delete=models.CASCADE)
    in_air_sec = models.FloatField()
    total_sec = models.FloatField()
    pilot = models.ForeignKey(Pilot,
                              on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, 
                                auto_now_add=False)
    mission = models.CharField(max_length=100)
    manager = MissionManager()
    objects = models.Manager()
    crash = models.IntegerField()
    eject = models.IntegerField()
    death = models.IntegerField()
    friendly_col_hits = models.IntegerField()
    friendly_col_kills = models.IntegerField()
    friendly_hits = models.IntegerField()
    friendly_kills = models.IntegerField()
    building_kills = models.IntegerField()
    ground_kills = models.IntegerField()
    heli_kills = models.IntegerField()
    fighter_kills = models.IntegerField()
    all_aircraft_kills = models.IntegerField()
    ship_kills = models.IntegerField()

    def __str__(self):
        return f"{self.mission} {self.date} {self.aircraft} {self.pilot}"
