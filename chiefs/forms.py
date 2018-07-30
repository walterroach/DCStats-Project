import datetime
import pytz
from django import forms
from stats.forms import LogFilter, MisForm
from stats.models import Pilot

class ChiefLogFilter(LogFilter):
    '''
    Inherits from stats.forms.LogFilter.  Adds pilot filter.
    '''
    pilot_filter = forms.ModelChoiceField(queryset=Pilot.objects.all(), required=False)

class ChiefMisForm(MisForm):
	'''
	Inherits from stats.forms.MisForm.  Adds ability to select pilot.
	'''
	pilot = forms.ModelChoiceField(queryset=Pilot.objects.all(), required=True)

