from django.db import models

class User(models.Model):
	clientid = models.CharField(max_length=32)
	name = models.CharField(max_length=50)
	callsign = models.CharField(max_length=30)

	def __str__(self):
		return f'{self.name}, "{callsign}"'

