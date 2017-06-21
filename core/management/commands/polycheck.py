from django.core.management import BaseCommand
from core.models import Polygon


class Command(BaseCommand):
    help = 'Show WKT of polygon'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        poly = Polygon.objects.all().first()
        print(str(poly.polygon.ogr))
