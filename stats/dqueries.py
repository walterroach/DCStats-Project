
from stats import models
from stats.models import Pilot, Total, Aircraft

class PilotTotal:
	def __init__(self, clientid):
		self.name = ''
		self.rank = ''
		self.in_air_hr = ''
		self.total_hr = ''

		x = Aircraft.manager.pilottotal(clientid)
		self.name = x.name
		self.rank = x.rank
		self.in_air_hr = x.in_air_hr
		self.total_hr = x.total_hr

	def __str__(self):
		return self.name
