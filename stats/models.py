from django.db import models


class Pilot(models.Model):
	clientid = models.CharField(max_length=32,
		primary_key=True)
	f_name = models.CharField(max_length=30)
	l_name = models.CharField(max_length=30)
	callsign = models.CharField(max_length=30)
	rank_id = models.ForeignKey('Rank', null=True, 
		on_delete=models.SET_NULL)

	def __str__(self):
		return f'{self.f_name} "{self.callsign}" {self.l_name}'

	def stats(self, clientid):
		self.air_hours = int

class Rank(models.Model):
	rank_choices = (
		("O1","O-1"),
		("O2","O-2"),
		("O3","O-3"),
		("O4","O-4"),
		("O5","O-5"),
		("O6","O-6")
		)
	rank = models.CharField(max_length=3,
		choices=rank_choices)
	AF_name = models.CharField(max_length = 30)
	Navy_name = models.CharField(max_length=30)

	def __str__(self):
		return self.rank

class Total(models.Model):
	aircraft = models.ForeignKey('Aircraft', 
		on_delete=models.CASCADE)
	pilot = models.ForeignKey('Pilot',
		on_delete=models.CASCADE)

class AircraftManager(models.Manager):
	def create_aircraft(self, aircraft, in_air_sec, total_sec, pilot):
		aircraft = self.create(aircraft=aircraft, in_air_sec=in_air_sec,
			total_sec=total_sec, pilot=pilot)
		
		return aircraft

class Aircraft(models.Model):
	aircraft = models.CharField(max_length=30)
	in_air_sec = models.FloatField()
	total_sec = models.FloatField()
	pilot = models.ForeignKey('Pilot',
		on_delete=models.CASCADE)
	objects = models.Manager()
	manager = AircraftManager()

	def __str__(self):
		return f"{self.aircraft} + {self.pilot}"


class Slmod_Total(models.Model):
	file = models.FileField(upload_to='SlmodStats/')
	name = models.CharField(max_length=30)

	def __str__ (self):
		return str(self.file)

class PilotTotal:
	def __init__(self, clientid):
		self.name = ''
		self.rank = ''
		self.in_air_hr = 0
		self.total_hr = 0

		pilot = Pilot.objects.get(clientid=clientid)
		self.name = str(pilot)
		self.rank = pilot.rank_id
		aircraft = Aircraft.objects.filter(pilot=clientid)
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
