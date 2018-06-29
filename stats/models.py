
'''
Django models for stats app
'''
from django.db import models
import datetime

class Pilot(models.Model):
    '''
    Django model class Pilot SQL table.
    '''
    clientid = models.CharField(max_length=32,
                                primary_key=True)
    f_name = models.CharField(max_length=30)
    l_name = models.CharField(max_length=30)
    callsign = models.CharField(max_length=30)
    rank_id = models.ForeignKey('Rank', null=True,
                                on_delete=models.SET_NULL)

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
        ("O6", "O-6")
        )
    rank = models.CharField(max_length=3,
                            choices=rank_choices)
    AF_name = models.CharField(max_length=30)
    Navy_name = models.CharField(max_length=30)

    def __str__(self):
        return self.rank


class AircraftManager(models.Manager):
    '''
    Django Manager class for editing Aircraft SQL table.
    '''
    def create_entry(self, aircraft, in_air_sec, total_sec, pilot, date=datetime.datetime.now()):
        '''
        Create a record in Aircraft SQL database and return it.
        '''
        aircraft = self.create(aircraft=aircraft, in_air_sec=in_air_sec,
                               total_sec=total_sec, pilot=pilot, date=date)
        return aircraft

class MissionManager(models.Manager):
    '''
    Django Manager class for editing Aircraft SQL table.
    '''
    def create_entry(self, aircraft, in_air_sec, total_sec, pilot, date=datetime.datetime.now()):
        '''
        Create a record in Mission SQL database and return it.
        '''
        aircraft = self.create(aircraft=aircraft, in_air_sec=in_air_sec,
                               total_sec=total_sec, pilot=pilot, date=date)
        return aircraft

class Aircraft(models.Model):
    '''
    Django Model class Aircraft SQL table
    '''
    aircraft = models.CharField(max_length=30)
    in_air_sec = models.FloatField()
    total_sec = models.FloatField()
    pilot = models.ForeignKey('Pilot',
                              on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=False, default=datetime.datetime.now())
    objects = models.Manager()
    manager = AircraftManager()

    def __str__(self):
        return f"{self.aircraft} + {self.pilot}"

class Mission(models.Model):
    '''
    Django Model class Mission SQL table
    '''
    aircraft = models.CharField(max_length=30)
    in_air_sec = models.FloatField()
    total_sec = models.FloatField()
    pilot = models.ForeignKey('Pilot',
                              on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, 
                                auto_now_add=False, 
                                default=datetime.datetime.now())

    manager = MissionManager()
    objects = models.Manager()

    def __str__(self):
        return f"{self.aircraft} + {self.pilot} + {self.date}"

class PilotTotal:
    '''
    Contains data for stats page Pilot Total view. 
    '''
    def __init__(self, clientid):
        self.name = ''
        self.rank = ''
        self.in_air_hr = 0
        self.total_hr = 0

        pilot = Pilot.objects.get(clientid=clientid)
        self.name = str(pilot)
        self.rank = pilot.rank_id
        aircraft = Mission.objects.filter(pilot=clientid)
        for a in aircraft:
            self.in_air_hr += (a.in_air_sec / 3600)
            self.total_hr += (a.total_sec / 3600)

    def __str__(self):
        return self.name

class AircraftTotal:
    def __init__(self, acmodel):
        self.name = ''
        self.rank = ''
        self.in_air_hr = 0
        self.total_hr = 0
        self.aircraft = acmodel.aircraft
        self.name = acmodel.pilot
        self.rank = acmodel.pilot.rank_id
        self.in_air_hr += (acmodel.in_air_sec / 3600)
        self.total_hr += (acmodel.total_sec / 3600)
