# decorators
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from stats.models import Pilot

def user_tz(function):
    def func_wrapper(request, *args, **kwargs):
        tzname = request.session.get('django_timezone')
        if not tzname:
            try:
                pilot = Pilot.objects.get(user=request.user)
                request.session['django_timezone'] = pilot.timezone
            except (ObjectDoesNotExist, TypeError) as e:
                pass
        return(function(request, *args, **kwargs))

    return func_wrapper