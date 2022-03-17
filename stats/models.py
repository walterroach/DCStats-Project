
'''
Django models for stats app
'''
import zoneinfo

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Pilot(models.Model):
    '''
    Django model class Pilot SQL table.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    clientid = models.CharField(max_length=32,
                                primary_key=True)
    callsign = models.CharField(max_length=30)


    def __str__(self):
        '''Return string value of Pilot'''
        try:
            name = f'{self.user.first_name} "{self.callsign}" {self.user.last_name}'
        except AttributeError:
            name = f'"{self.callsign}"'

        return name

class UserProfile(models.Model):
    '''
    OnetoOne extension of Django User Model
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    rank_id = models.ForeignKey('Rank', null=True, blank=True,
                                on_delete=models.SET_NULL,
                                default=1)
    tz_choices = ((tz, tz) for tz in zoneinfo.available_timezones())
    tz_choices = tuple(tz_choices)
    timezone = models.CharField(max_length=32, default='UTC', choices=tz_choices)

    def __str__(self):
        '''Return string value of Pilot'''
        name = f'{self.user.username} Profile'

        return name

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
        return(f'{self.file}')

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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()