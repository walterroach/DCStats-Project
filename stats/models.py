
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
    def create_entry(self, aircraft, in_air_sec, total_sec, pilot, mission, date):
        '''
        Create a record in Mission SQL database and return it.
        '''
        # aircraft = Aircraft.objects.get(aircraft=aircraft, pilot=pilot)
        # try:
        print('MissionManager.create_entry')
        mission = self.create(aircraft=aircraft, in_air_sec=in_air_sec,
                              total_sec=total_sec, pilot=pilot, mission=mission, date=date)
        # except ValueError:
        #     print(aircraft)
        #     Aircraft.manager.create_entry(aircraft)
        return mission

class Aircraft(models.Model):
    '''
    Django Model class Aircraft SQL table
    '''
    aircraft = models.CharField(max_length=30, primary_key=(True))
    # pilot = models.ForeignKey('Pilot',
    #                           on_delete=models.CASCADE)
    objects = models.Manager()
    manager = AircraftManager()

    def __str__(self):
        return f"Aircraft Object {self.aircraft}"

class Mission(models.Model):
    '''
    Django Model class Mission SQL table
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

    def __str__(self):
        return f"Mission Object {self.aircraft} + {self.pilot} + {self.date}"

class Total:
    def __init__(self, clientid="", aircraft=""):
        self.name = ""
        self.rank = ""
        self.aircraft = ""
        self.in_air_hr = 0
        self.total_hr = 0

class PilotTotal(Total):
    '''
    Contains data for stats page Pilot Total view. 
    '''
    def __init__(self, clientid):
        super().__init__(self)
        pilot = Pilot.objects.get(clientid=clientid)
        self.name = str(pilot)
        self.rank = pilot.rank_id
        aircraft = Mission.objects.filter(pilot=clientid)
        for a in aircraft:
            self.in_air_hr += (a.in_air_sec / 3600)
            self.total_hr += (a.total_sec / 3600)

    def __str__(self):
        return self.name

class AircraftTotal(Total):
    def __init__(self, aircraft):
        super().__init__(self)
        # self.name = str(aircraft.mission.pilot)
        # self.rank = aircraft.pilot.rank_id
        self.aircraft = aircraft.aircraft        
        pilots = Mission.objects.filter(aircraft=aircraft)
        for p in pilots:
            self.in_air_hr += (p.in_air_sec / 3600)
            self.total_hr += (p.total_sec / 3600)

