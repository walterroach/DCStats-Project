#forms.py
import datetime
import pytz
from django import forms
from django.forms import ModelForm
from stats.models import *
from django.forms import modelformset_factory
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

def not_future(date):
	if date > datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=1):
		raise forms.ValidationError('The end date date cannot be in the future')
		return date

class StatsOptions(forms.Form):
	group_by_choices = [("pilot","Pilot"), ("aircraft","Aircraft"), ("mission__name","Mission"), ("day","Date")]
	# group_by2_choices = ['Pilot', 'Aircraft', 'Mission', 'Date']
	group_by = forms.MultipleChoiceField(label='Group By', choices=group_by_choices, initial='Pilot')
	aircraft_choices = [('All','All')]
	aircrafts = Aircraft.objects.all().order_by('aircraft')
	for aircraft in aircrafts:
		aircraft_choices.append((aircraft.aircraft, aircraft.aircraft))
	pilot_choices = [('All','All')]
	pilots = Pilot.objects.all().order_by('user__first_name')
	for pilot in pilots:
		pilot_choices.append((pilot.clientid, str(pilot)))
	# group_by2 = forms.ChoiceField(label='and Group By', choices=group_by2_choices, widget=forms.Select)
	start_date = forms.DateTimeField(widget=forms.SelectDateWidget(years=[2017,2018]), initial=(datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)))
	end_date = forms.DateTimeField(initial=datetime.datetime.now(pytz.utc), widget=forms.SelectDateWidget(years=[2018,2017]), validators=[not_future])
	aircraft_filter = forms.ChoiceField(label='Aircraft Filter', initial='All', choices=aircraft_choices, widget=forms.Select())
	pilot_filter = forms.ChoiceField(label="Pilot Filter", choices=pilot_choices, widget=forms.Select())
	sort_by_choices = [('pilot__user__first_name','Pilot'),('pilot__rank_id','Rank'),('aircraft','Aircraft'),('mission__name','Mission'),('-day', 'Date'),('-in_air_hours','In Air Hours'),
					   ('-hours_on_server', 'Hours On Server'),('-losses', 'Losses'),('-all_aircraft_kills', 'Air Kills'),
					   ('-surface_kills', 'Surface Kills')]
	sort_by = forms.ChoiceField(label='Sort By', choices=sort_by_choices, widget=forms.Select())

class LogFilter(forms.Form):
	start = timezone.localtime() - datetime.timedelta(days=7)
	start_date = forms.DateTimeField(widget=forms.SelectDateWidget(years=[2017,2018]), initial=(start))
	end_date = forms.DateTimeField(initial=datetime.datetime.now(pytz.utc), widget=forms.SelectDateWidget(years=[2018,2017]))

	def clean_end_date(self):
		end_date = self.cleaned_data['end_date']
		end_date = end_date.replace(hour=23, minute=59, second=59)
		return end_date

class LogForm(ModelForm):
	class Meta:
		model = Stats
		fields = ['landings', 'traps', 'aar', 'aircraft_kills',
				  'ground_kills', 'losses']
		labels = {'aar':'AAR'}
		