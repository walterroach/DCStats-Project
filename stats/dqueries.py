
from stats import models
from stats.models import Pilot, Total, Aircraft

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
