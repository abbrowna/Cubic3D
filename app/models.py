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
class Material(models.Model):
    acronym = models.CharField(primary_key=True, max_length=5, verbose_name = "Material Acronym")
    density = models.FloatField()
    ppg = models.IntegerField(verbose_name = "Price per gram")
    color1 = models.CharField(max_length=5, blank=True)
    color2 = models.CharField(max_length=5, blank=True)
    color3 = models.CharField(max_length=5, blank=True)
    color4 = models.CharField(max_length=5, blank=True)
    color5 = models.CharField(max_length=5, blank=True)

    def available_colors(self):
        colors=[]
        for color_no in range(1,6,1):
            fieldname = "color{}".format(color_no)
            color=getattr(self, fieldname)
            if color:
                colors.append(color)
        return colors


class PrintRequest(models.Model):
    description = models.CharField(max_length=255, blank=True, verbose_name = "Descriptive name")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thing = models.FileField(upload_to='thingstemp/%Y/%m/',
                             validators=[FileExtensionValidator(['stl'],'Please upload your file as a .STL Most CAD software are capable of exporting models in this format.')])
    uploaded_at = models.DateTimeField(auto_now_add=True,)
    infill_choices=(
        ('ART','Artistic/Aestetic'),('MECH','Mechanical')
    )
    material = models.ForeignKey(Material, on_delete=models.CASCADE, default='PLA')
    purpose = models.CharField(max_length=5,choices=infill_choices,default='ART')
    color = models.CharField(max_length=10)
    color_combo = models.TextField(blank=True,)
    scale = models.FloatField(default=100)
    quantity = models.IntegerField(blank=True, default=1)
    further_requests = models.TextField(blank=True,)
    confirmation_sent=models.BooleanField(default=False)
    grouped=models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    confirmation_date = models.DateTimeField(blank=True, null=True,)
    final_price = models.IntegerField(blank=True, null=True)
    printed = models.BooleanField(default=False)
    receipted = models.BooleanField(default=False)
    
    #def slicemass(self):
    #    from app.stlprocessing import slicedweight
    #    return slicedweight(self.thing.path,self.material.density)

    def thing_price(self):
        from app.stlprocessing import slicedweight
        output,mass = slicedweight(self.thing.path,self.material.density)
        price = (int(math.ceil(mass))*self.material.ppg)
        return mass,int(math.ceil(price/50.0)*50)
    
    def subtotal(self):
        return self.final_price*self.quantity

class GroupedPrintRequest(models.Model):
    printrequest = models.ForeignKey(PrintRequest, on_delete=models.CASCADE)

class Invoice(models.Model):
    number = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bill_to = models.CharField(max_length=100, blank=True)
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)

class GroupRecord(models.Model):
    id_string = models.CharField(max_length=100, primary_key=True)
    def id_list(self):
        request_IDs = self.id_string[1:len(self.id_string)-1].split(", ")
        IDs = []
        for i in request_IDs:
            IDs.append(int(i))
        return IDs

class Quote(models.Model):
    thing = models.FileField(upload_to='thingstemp/%Y/%m/',
                             validators=[FileExtensionValidator(['stl'],'Please upload your file as a .STL Most CAD software are capable of exporting models in this format.')])
    infill_choices=(
        ('ART','Artistic/Aestetic'),('MECH','Mechanical')
    )
    material = models.ForeignKey(Material, on_delete=models.CASCADE, default='PLA')
    purpose = models.CharField(max_length=5,choices=infill_choices,default='ART')
    color = models.CharField(max_length=10)
    scale = models.FloatField(default=100)
    def slicemass(self):
        from app.stlprocessing import slicedweight
        return slicedweight(self.thing.path,self.material.density)

    def thing_price(self):
        from app.stlprocessing import slicedweight
        output,mass = slicedweight(self.thing.path,self.material.density)
        price = (int(math.ceil(mass))*self.material.ppg)
        return mass,int(math.ceil(price/50.0)*50)


class ThingOrders(models.Model):
    upload_id = models.IntegerField()
    description = models.CharField(max_length=255, blank=True, verbose_name = "Descriptive name")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thing = models.FileField(upload_to='orderedthings/%Y/%m/%d/')
    confirmed_on = models.DateTimeField(auto_now_add=True)    
    material = models.CharField(max_length=5)
    purpose = models.CharField(max_length=5)
    color = models.CharField(max_length=10)
    color_combo = models.TextField(blank=True,)
    scale = models.FloatField(default=False,)
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







