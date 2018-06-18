from django.core.management.base import BaseCommand, CommandError
from stats import models




class Command(BaseCommand):
	def handle(self, **options):
		stats_json = models.Slmod_Total.objects.all
		mylist = []
		for x in stats_json:
			mylist.append(x.name)
		return self.stdout.write(self.style.SUCCESS(f'retrieved {mylist}'))

	#totals = Total.objects.all()
	#for pilot in totals:
	#	pilot.
