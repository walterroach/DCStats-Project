import subprocess

from django.core.management.base import BaseCommand, CommandError


def sync_stats():
    filepath = "C:\\Users\\Walter\\Desktop\\DCStats Django\\DCStats-Project\\willshousesync.bat"
    p = subprocess.Popen(filepath)

    print(p.returncode)


class Command(BaseCommand):
    def handle(self, **options):
        return sync_stats()
