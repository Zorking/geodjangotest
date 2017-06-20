from django.contrib.gis.db import models as gis_models
from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    location = gis_models.PointField(geography=True, null=True)
    gis = gis_models.GeoManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.name
