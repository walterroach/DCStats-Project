from django.contrib import admin
from .models import Pilot, Rank, Aircraft

admin.site.register(Pilot)
admin.site.register(Rank)
admin.site.register(Aircraft)