# decorators
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from stats.models import Pilot, UserProfile

def user_tz(function):
    def func_wrapper(request, *args, **kwargs):
        tzname = request.session.get('django_timezone')
        if not tzname:
            try:
                userprofile = UserProfile.objects.get(user=request.user)
                request.session['django_timezone'] = userprofile.timezone
            except (ObjectDoesNotExist, TypeError) as e:
                pass
        return(function(request, *args, **kwargs))

    return func_wrapper