from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.db import models as gis_models



class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class Location(gis_models.Model):
    provider = gis_models.ForeignKey(Provider, to_field='name', on_delete=gis_models.CASCADE)
    name = gis_models.CharField(max_length=254)
    price = gis_models.DecimalField(max_digits=10, decimal_places=2)
    polygon = gis_models.PolygonField()

    def __str__(self):
        return self.name