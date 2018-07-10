#forms.py
import datetime
from django import forms
from stats.models import *

class StatsOptions(forms.Form):
	group_by_choices = [("Pilot","Pilot"), ("Aircraft","Aircraft"), ("Mission","Mission"), ("Date","Date")]
	# group_by2_choices = ['Pilot', 'Aircraft', 'Mission', 'Date']
	group_by = forms.MultipleChoiceField(label='Group By', choices=group_by_choices, initial='Pilot', widget=forms.CheckboxSelectMultiple())
	aircraft_choices = []
	aircrafts = Aircraft.objects.all()
	for aircraft in aircrafts:
		aircraft_choices.append((aircraft.aircraft, aircraft.aircraft))
	# group_by2 = forms.ChoiceField(label='and Group By', choices=group_by2_choices, widget=forms.Select)
	start_date = forms.DateField(widget=forms.SelectDateWidget(years=[2017,2018]))
	end_date = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(years=[2018,2017]))
	aircraft_filter = forms.ChoiceField(label='Aircraft Filter', choices=aircraft_choices, widget=forms.Select())
	sort_by_choices = [('pilot','Pilot'),('rank','Rank'),('aircraft','Aircraft'),('in_air_hours','In Air Hours'),
					   ('hours_on_server', 'Hours On Server'),('losses', 'Losses'),('all_aircraft_kills', 'Air Kills'),
					   ('surface_kills', 'Surface Kills')]
	sort_by = forms.ChoiceField(label='Sort By', choices=sort_by_choices, widget=forms.Select())