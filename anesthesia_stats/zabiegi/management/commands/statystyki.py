from django.core.management.base import BaseCommand

from zabiegi import core


class Command(BaseCommand):
    help = "Wyświetla statystyki"

    def handle(self, *args, **kwargs):
        core.pokaz_statystyki()
