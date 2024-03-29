# decorators
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from stats.models import Pilot, Stats, UserProfile


def user_tz(function):
    def func_wrapper(request, *args, **kwargs):
        tzname = request.session.get("django_timezone")
        if not tzname:
            try:
                userprofile = UserProfile.objects.get(user=request.user)
                request.session["django_timezone"] = userprofile.timezone
            except (ObjectDoesNotExist, TypeError) as e:
                print(e)
        return function(request, *args, **kwargs)

    return func_wrapper


def user_must_own_stat(function):
    def func_wrapper(request, *args, **kwargs):
        pilot = Pilot.objects.get(user=request.user)
        stat = Stats.objects.get(pk=request.GET["stat"])
        if pilot != stat.pilot:
            return redirect("unauthorized")
        else:
            return function(request, *args, **kwargs)

    return func_wrapper
