from django.contrib import admin
from .models import Pilot, Rank, Aircraft, Mission, Stats, UserProfile


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_filter = ("in_process", "date")


admin.site.register(Pilot)
admin.site.register(Rank)
admin.site.register(Aircraft)
admin.site.register(Stats)
# admin.site.register(Mission)
admin.site.register(UserProfile)
