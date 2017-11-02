"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
import math

# Create your models here.

class Tempthings(models.Model):
    description = models.CharField(max_length=255, blank=True, verbose_name = "Descriptive name")
    user = models.ForeignKey(User)
    thing = models.FileField(upload_to='thingstemp/%Y/%m/',
                             validators=[FileExtensionValidator(['stl'],'Please export your file as a .STL object then upload it. If your unable, Email your file to us instead')])
    uploaded_at = models.DateTimeField(auto_now_add=True,)
    material_choices=(
        ('PLA','PLA'),('PETG','PETG')
    )
    infill_choices=(
        ('ART','Artistic/Aestetic'),('MECH','Mechanical')
    )
    color_choices=(
        ('GRN','Green'),('BLK','Black'),('WHT','White'),('COMBO','green-black combo')
        )
    material = models.CharField(max_length=5,choices=material_choices,default='PLA')
    purpose = models.CharField(max_length=5,choices=infill_choices,default='ART')
    color = models.CharField(max_length=10,choices=color_choices,default='GRN')
    color_combo = models.TextField(blank=True,)
    scale_info = models.TextField(blank=True,)
    further_requests = models.TextField(blank=True,)
    confirmation_sent=models.BooleanField(default=False)
    
    def slicemass(self):
        from app.stlprocessing import slicedweight
        if self.material == 'PETG':
            density = 1.27
        elif self.material == 'PLA':
            density = 1.25
        return slicedweight(self.thing.path,density)

    def thing_price(self):
        from app.stlprocessing import slicedweight
        if self.material == 'PETG':
            density = 1.27
        elif self.material == 'PLA':
            density = 1.25
        output,mass = slicedweight(self.thing.path,density)
        price = (int(math.ceil(mass))*15)
        return mass,int(math.ceil(price/50.0)*50)


class ThingOrders(models.Model):
    upload_id = models.IntegerField()
    description = models.CharField(max_length=255, blank=True, verbose_name = "Descriptive name")
    user = models.ForeignKey(User)
    thing = models.FileField(upload_to='orderedthings/%Y/%m/%d/')
    confirmed_on = models.DateTimeField(auto_now_add=True)    
    material_choices=(
        ('PLA','PLA'),('PETG','PETG')
    )
    infill_choices=(
        ('ART','Artistic/Aestetic'),('MECH','Mechanical')
    )
    color_choices=(
        ('GRN','Green'),('BLK','Black'),('WHT','White'),('COMBO','green-black combo')
        )
    material = models.CharField(max_length=5,choices=material_choices,default='PLA')
    purpose = models.CharField(max_length=5,choices=infill_choices,default='ART')
    color = models.CharField(max_length=10,choices=color_choices,default='GRN')
    color_combo = models.TextField(blank=True,)
    scale_info = models.TextField(blank=True,)
    further_requests = models.TextField(blank=True,)
    printed = models.BooleanField(default=False,)

    def thing_price(self):
        from app.stlprocessing import getmass
        if self.material == 'PETG':
            density = 1.27
        elif self.material == 'PLA':
            density = 1.25
        mass=getmass(self.thing.path,density)
        print(math.ceil(mass))
        return(int(math.ceil(mass))*12)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile=models.CharField(max_length=10, default=0)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()







