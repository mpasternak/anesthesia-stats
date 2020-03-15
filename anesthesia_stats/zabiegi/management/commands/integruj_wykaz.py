from django.core.management.base import BaseCommand

from zabiegi import core


class Command(BaseCommand):
    help = "Integruje zaimportowane zabiegi"

    def handle(self, *args, **kwargs):
        core.integruj_wszystko()
