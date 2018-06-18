from django.db import models

class Pilot(models.Model):
	clientid = models.CharField(max_length=32,
		primary_key=True)
	f_name = models.CharField(max_length=30)
	l_name = models.CharField(max_length=30)
	callsign = models.CharField(max_length=30)
	rank_id = models.ForeignKey('Rank', null=False, 
		on_delete=models.CASCADE)

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
	in_air = models.IntegerField()
	total = models.IntegerField()
	pilot = models.ForeignKey('Pilot', null=True,
		on_delete=models.SET_NULL)

class Slmod_Total(models.Model):
	file = models.FileField(upload_to='SlmodStats/%Y/%m/')
	name = models.CharField(max_length=30)

	def __str__ (self):
		return str(self.file)