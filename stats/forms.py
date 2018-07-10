#forms.py
import datetime
from django import forms
from stats.models import *

def not_future(date):
	if date > datetime.date.today():
		raise forms.ValidationError('The end date date cannot be in the future')
		return date

class StatsOptions(forms.Form):
	group_by_choices = [("pilot","Pilot"), ("aircraft","Aircraft"), ("mission","Mission"), ("date","Date")]
	# group_by2_choices = ['Pilot', 'Aircraft', 'Mission', 'Date']
	group_by = forms.MultipleChoiceField(label='Group By', choices=group_by_choices, initial='Pilot')
	aircraft_choices = [('All','All')]
	aircrafts = Aircraft.objects.all().order_by('aircraft')
	for aircraft in aircrafts:
		aircraft_choices.append((aircraft.aircraft, aircraft.aircraft))
	pilot_choices = [('All','All')]
	pilots = Pilot.objects.all().order_by('f_name')
	for pilot in pilots:
		pilot_choices.append((pilot.clientid, str(pilot)))
	# group_by2 = forms.ChoiceField(label='and Group By', choices=group_by2_choices, widget=forms.Select)
	start_date = forms.DateField(widget=forms.SelectDateWidget(years=[2017,2018]), initial=(datetime.datetime.today() - datetime.timedelta(days=7)))
	end_date = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(years=[2018,2017]), validators=[not_future])
	aircraft_filter = forms.ChoiceField(label='Aircraft Filter', initial='All', choices=aircraft_choices, widget=forms.Select())
	pilot_filter = forms.ChoiceField(label="Pilot Filter", initial='All', choices=pilot_choices, widget=forms.Select())
	sort_by_choices = [('pilot__f_name','Pilot'),('pilot__rank_id','Rank'),('aircraft','Aircraft'),('mission','Mission'),('date', 'Date'),('-in_air_hours','In Air Hours'),
					   ('-hours_on_server', 'Hours On Server'),('-losses', 'Losses'),('-all_aircraft_kills', 'Air Kills'),
					   ('-surface_kills', 'Surface Kills')]
	sort_by = forms.ChoiceField(label='Sort By', choices=sort_by_choices, widget=forms.Select())