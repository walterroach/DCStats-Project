import datetime
from django.utils import timezone
import pytz
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from stats.models import Pilot
from home.forms import SignUpForm, UserProfileForm, PilotProfileForm
from django.core.exceptions import ObjectDoesNotExist
import datetime
import pytz
from home.decorators import user_tz

@user_tz
def home(request):
    time = datetime.datetime.now(pytz.utc)
    return render(request, 'home/home.html', {'time':time})

def logout_view(request):
    logout(request)
    return render(request, 'home/logout.html')
    
def login(request):
    return render(request, 'home/login.html')

def inactive(request):
    return render(request, 'home/inactive.html')
    
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)
            auth_login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'home/signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        userform=UserProfileForm(request.POST, instance=request.user)
        try:
            pilot = Pilot.objects.get(user=request.user)
            pilotform=PilotProfileForm(request.POST, instance=pilot)
            pilot_valid = pilotform.is_valid()
            if pilot_valid:
                pilotform.save()
            request.session['django_timezone'] = pilot.timezone
        except ObjectDoesNotExist:
            pilotform = None
            pilot_valid = True
        user_valid = userform.is_valid()
        if pilot_valid and user_valid:
            change = 'Changes Submitted'
            print("PILOT SAVED!")
        else:
            print("PILOT INVALID")
        if user_valid:
            userform.save()
        else:
            print("USER INVALID")
        
    else:
        try:
            pilot = Pilot.objects.get(user=request.user)
            pilotform = PilotProfileForm(instance=pilot)
        except ObjectDoesNotExist:
            pilotform = None
        userform = UserProfileForm(instance=request.user)        
        change = ''

    return render(request, 'home/profile.html', {'userform':userform, 'change':change, 'pilotform':pilotform})


# def profile(request):
#     if request.method == 'POST':
#         userform=UserProfileForm(request.POST, instance=request.user)
#         request.session['django_timezone'] = request.POST['timezone']
#         if userform.is_valid():
#             userform.save()
#             change = 'Change Submitted'
#             userform=UserProfileForm(instance=request.user)
#         if not userform.is_valid():
#             change = 'Problem sumbitting request, please contact administrator'
#     else:
#         userform = UserProfileForm(instance=request.user)
#         change = ''
#     try:
#         pilot = Pilot.objects.get(user=request.user)
#         pilotform=PilotProfileForm(instance=pilot)
#     except ObjectDoesNotExist:
#         pilotform = None
#         pilot = {'rank_id':"Welcome Guest!"}
    
#     return render(request, 'home/profile.html', {'userform':userform, 'pilot':pilot, 'change':change, 'pilotform':pilotform,})

def get_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
    else:
        return render(request, 'stats/timezone.html', {'timezones': pytz.common_timezones})