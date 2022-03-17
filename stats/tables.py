# tables.py

import django_tables2 as tables
from .models import Stats


class StatTable(tables.Table):
    class Meta:
        model = Stats
        template_name = "django_tables2/bootstrap.html"
        attrs = {
            "class": "table table-striped table-bordered table-responsive ml-1 mt-2 bg-light"
        }
