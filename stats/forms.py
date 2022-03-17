'''
stats.forms
'''
import datetime
from django import forms
from django.forms import ModelForm
from stats.models import Stats, Pilot, Aircraft, Mission
from django.utils import timezone

class StatsOptions(forms.Form):
    '''
    **Validation**
    Django form, inherits from django.forms.Form
    '''
    group_by_choices = [("pilot__callsign", "Pilot"),
                        ("aircraft", "Aircraft"),
                        ("mission__name", "Mission")]
    group_by = forms.MultipleChoiceField(label='Group By',
                                         choices=group_by_choices,
                                         initial='Pilot')
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={'id':'start_date'}))
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs={'id':'end_date'}))
    aircraft_filter = forms.ModelChoiceField(queryset=Aircraft.objects.all(), required=False)
    pilot_filter = forms.ModelChoiceField(queryset=Pilot.objects.all(), required=False)

    def clean_end_date(self):
        '''
        **Validation**
        Replaces time with 23:59:59 during form validation
        '''
        end_date = self.cleaned_data['end_date']
        end_date = end_date.replace(hour=23, minute=59, second=59)
        return end_date

class LogFilter(forms.Form):
    '''
    Django form.  Inherits from django.forms.Form
    '''
    start = timezone.localtime() - datetime.timedelta(days=7)
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={'id':'start_date'}))
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs={'id':'end_date'}))
    unlogged_only = forms.BooleanField(required=False, initial=False)

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        end_date = end_date.replace(hour=23, minute=59, second=59)
        return end_date

    def clean_unlogged_only(self):
        unlogged_only = self.cleaned_data['unlogged_only']
        if unlogged_only:
            unlogged_only = 1
        else:
            unlogged_only = 0
        return unlogged_only
        
class LogForm(ModelForm):
    '''
    Django model form.  Inherits from django.forms.ModelForm
    '''
    class Meta:
        model = Stats
        fields = ['landings', 'traps', 'aar', 'aircraft_kills',
                  'ground_kills', 'losses']
        labels = {'aar':'AAR'}

class NewLogForm(ModelForm):
	total_minutes = forms.IntegerField(min_value=0)

	class Meta:
		model = Stats
		fields = ['landings', 'traps', 'aar', 'aircraft_kills',
				  'ground_kills', 'losses',]
		labels = {'aar':'AAR'}


class MisForm(ModelForm):
	aircraft = forms.ModelChoiceField(queryset=Aircraft.objects.all().order_by('aircraft'), required=True)
	class Meta:
		model = Mission
		fields = ['name', 'date', 'file', 'in_process']
		labels = {'name':'Entry Type'}
		widgets = {
			'date': forms.TextInput(attrs={'id':'mis_date'}),
			'file': forms.HiddenInput(attrs={'value':'external_entry'}),
			'in_process':forms.HiddenInput(attrs={'value':0}),
			'name': forms.Select(choices=[('Other', 'Other'),
										  ('Blue Flag', 'Blue Flag'),
										  ('Dynamic DCS', 'Dynamic DCS'),
										  ('Other Server', 'Other Server'),
										  ('21st Server Error', '21st Server Error'),])
		}
		
