import datetime
import pytz
from django import forms
from stats.forms import LogFilter, MisForm
from stats.models import Pilot

class ChiefLogFilter(LogFilter):
    '''
    Inherits from stats.forms.LogFilter.  Adds pilot filter.
    '''
    pilot = forms.ModelChoiceField(queryset=Pilot.objects.all().order_by('callsign'), required=False, label='Pilot Filter')

class ChiefMisForm(MisForm):
	'''
	Inherits from stats.forms.MisForm.  Adds ability to select pilot.
	'''
	pilot = forms.ModelChoiceField(queryset=Pilot.objects.all(), required=True)

