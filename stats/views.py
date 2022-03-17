"""
###########
stats.views
###########
"""
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.utils import timezone

from home.decorators import user_must_own_stat, user_tz
from stats import query

from .forms import LogFilter, LogForm, MisForm, NewLogForm, StatsOptions
from .models import Mission, Pilot, Stats


@user_tz
@login_required
def pilot_stats(request):
    """
    Displays the Leaderboard page

    **Context**

    form
        An instance of forms.StatsOptions

    stats
        dict from query.execute on :model:'stats.Stats'

    start_date
        The currently selected start_date in form

    end_date
        The currently selected end_date in form

    Template
        stats/leaderboard.html
    """
    try:
        user = request.user
        user = Pilot.objects.get(user=user)
        if request.method == "POST":
            form = StatsOptions(request.POST)
            print(f"Request:  {request.POST}")
            if form.is_valid():
                options = form.cleaned_data
                stats = query.execute(options)
                print(f"OPTIONS:{options}")
                start_date = options["start_date"]
                end_date = options["end_date"]
                return render(
                    request,
                    "stats/leaderboard.html",
                    {
                        "form": form,
                        "stats": stats,
                        "start_date": start_date.date,
                        "end_date": end_date.date,
                    },
                )
        else:
            start_date = timezone.localtime()
            start_date = query.last_week(start_date)
            end_date = timezone.localtime().replace(hour=0, minute=0, second=0)
            end_date = query.end_day(end_date)
            form = StatsOptions(
                initial={
                    "group_by": ["pilot__callsign"],
                    "start_date": start_date.date(),
                    "end_date": end_date.date(),
                }
            )
            options = {
                "group_by": ["pilot__callsign"],
                "start_date": start_date,
                "end_date": end_date,
                "aircraft_filter": None,
                "pilot_filter": None,
            }
            print(options)
            stats = query.execute(options)

        return render(
            request,
            "stats/leaderboard.html",
            {
                "form": form,
                "stats": stats,
                "start_date": start_date.date,
                "end_date": end_date.date,
            },
        )
    except ObjectDoesNotExist:
        return redirect("inactive")


@user_must_own_stat
@login_required
@user_tz
def log_entry(request):
    """
    Displays an individual :model:'stats.Stats' for editing

    **Context**
    ''stat''
        An instance of :model:'stats.Stats'

    ''hours''
        Dict holding hours conversion from :model:'stats.Stats.in_air_sec'
        and :model:'stats.Stats.total_sec'

    ''logform''
        An instance of forms.LogForm

    **Template**
        :template:'stats/log_entry.html'
    """
    if request.method == "POST":
        stat = Stats.objects.get(pk=request.POST["statid"])
        if "total_minutes" in request.POST:
            logform = NewLogForm(request.POST, instance=stat)
        else:
            logform = LogForm(request.POST, instance=stat)
        if logform.is_valid():
            stat = logform.save(commit=False)
            stat.new = 0
            try:
                stat.total_sec = logform.cleaned_data["total_minutes"] * 60
                stat.in_air_sec = (logform.cleaned_data["total_minutes"] * 0.8) * 60
            except KeyError:
                pass
            stat.save()
            change = "Change Submitted"
    else:
        change = ""
        stat = Stats.objects.get(pk=request.GET["stat"])
        if stat.mission.name in [
            "Blue Flag",
            "Dynamic DCS",
            "Other Server",
            "21st Server Error",
            "Other",
        ]:
            logform = NewLogForm(instance=stat)
        else:
            logform = LogForm(instance=stat)
    hours = {}
    hours["in_air"] = stat.in_air_sec / 3600
    hours["on_server"] = stat.total_sec / 3600
    return render(
        request,
        f"stats/log_entry.html",
        {
            "stat": stat,
            "hours": hours,
            "logform": logform,
            "change": change,
        },
    )


@login_required
@user_tz
def pilot_log(request):
    """
    Displays instances of :model:'stats.Stats' related to currently logged in user

    **Context**
    ''log_filter''
        An instance of forms.LogFilter

    ''logs''
        A queryset of :model:'stats.Stats' from query.new_stats

    **Template**
        :template:'stats/pilot_log.html'
    """
    try:
        pilot = Pilot.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect("inactive")
    end_date = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = query.end_day(end_date)
    date = end_date
    mis_form = MisForm(initial={"date": date.date})
    if request.method == "POST":
        log_filter = LogFilter(request.POST)
        if log_filter.is_valid():
            clean = log_filter.cleaned_data
            clean["pilot"] = pilot
            logs = query.new_stats(clean)
            return render(
                request,
                "stats/pilot_log.html",
                {"log_filter": log_filter, "mis_form": mis_form, "logs": logs},
            )
    start_date = timezone.localtime()
    start_date = query.before_start(start_date)
    log_filter = LogFilter(
        initial={
            "start_date": start_date.date,
            "end_date": end_date.date,
            "unlogged_only": False,
        }
    )
    options = {
        "unlogged_only": 0,
        "start_date": start_date,
        "end_date": end_date,
        "pilot": pilot.pk,
    }
    print(f"OPTIONS: {options}")
    logs = query.new_stats(options)
    return render(
        request,
        "stats/pilot_log.html",
        {"log_filter": log_filter, "mis_form": mis_form, "logs": logs},
    )


@login_required
def new_log(request):
    if request.method == "POST":
        mis_form = MisForm(request.POST)
        if mis_form.is_valid():
            mis = Mission.objects.get_or_create(
                name=mis_form.cleaned_data["name"],
                date=mis_form.cleaned_data["date"],
                file=mis_form.cleaned_data["file"],
            )
            new_mis = mis[0]
            new_mis.in_process = 0
            new_mis.save()
        pilot = Pilot.objects.get(user=request.user)
        stat = Stats.objects.create(
            mission=new_mis, pilot=pilot, aircraft=mis_form.cleaned_data["aircraft"]
        )
        return redirect(f"/stats/log_entry?stat={stat.pk}")


def privacy(request):
    return render(
        request,
        "stats/privacy_policy.html",
    )

    #     logform = LogForm(request.POST, instance=stat)
    #     if logform.is_valid():
    #         stat = logform.save(commit=False)
    #         stat.new = 0
    #         stat.save()
    # else:
    #     stat = Stats.objects.get(pk=request.GET['stat'])
    #     logform = LogForm(instance=stat)
    #     hours = {}
    #     hours['in_air'] = stat.in_air_sec / 3600
    #     hours['on_server'] = stat.total_sec / 3600
    # return render(request,
    #               f'stats/log_entry.html',
    #               {
    #                   'stat':stat,
    #                   'hours':hours,
    #                   'logform':logform
    #               }
    #              )
