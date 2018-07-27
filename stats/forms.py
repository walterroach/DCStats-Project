'''
stats.forms
'''
import datetime
import pytz
from django import forms
from django.forms import ModelForm
# from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from stats.models import Stats, Pilot, Aircraft

class StatsOptions(forms.Form):
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
        end_date = self.cleaned_data['end_date']
        end_date = end_date.replace(hour=23, minute=59, second=59)
        return end_date

class LogFilter(forms.Form):
    start = timezone.localtime() - datetime.timedelta(days=7)
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={'id':'start_date'}))
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs={'id':'end_date'}))

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
