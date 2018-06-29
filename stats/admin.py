from django.contrib import admin
from .models import Pilot, Rank, Aircraft, Mission

admin.site.register(Pilot)
admin.site.register(Rank)
admin.site.register(Aircraft)
admin.site.register(Mission)