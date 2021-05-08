"""
Definition of models for the store application (store).
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

dia_choices = [(1.75, '1.75'),(2.85, '2.85')]
mass_choices = [(250, '250g'),(500,'500g'),(750, '750g'),(1000, '1Kg')]

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length = 30, primary_key=True)

class Material(models.Model):
    name = models.CharField(max_length = 20, primary_key=True)
    def __str__(self):
        return self.name

class Filament(models.Model):
    diameter = models.DecimalField(max_digits = 3, decimal_places=2, choices=dia_choices)
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE)
    stock = models.IntegerField()
    material = models.ForeignKey(Material, on_delete = models.CASCADE)
    color = models.CharField(max_length = 10)
    net_weight = models.IntegerField(choices = mass_choices)
    price = models.IntegerField()
    image = models.ImageField(blank=True)
    characteristics = models.TextField(blank=True)
    print_temp = models.CharField(max_length = 15, blank = True)
    bed_temp = models.CharField(max_length = 15, blank = True)

    def __str__(self):
        return str(self.diameter) + 'mm' + ' ' + self.color + ' ' + self.material.name

class Region(models.Model):
    region = models.CharField(max_length = 50)
    cost = models.IntegerField()
    
    def __str__(self):
        return self.region

class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, blank=True)
    address = models.TextField(max_length = 100, blank=False)
    phone = models.CharField(max_length = 50)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    company = models.CharField(max_length = 100, blank=True )
    email = models.EmailField()
    time = models.DateTimeField(auto_now_add=True)
    region = models.ForeignKey(Region, on_delete = models.SET_NULL, null=True, default=1)
    paid = models.BooleanField(default = False)
    delivered = models.BooleanField(default = False)
    item_total = models.IntegerField(default = 0)
    delivery_fee = models.IntegerField(default = 350)
    
    alt_name = models.CharField(max_length = 50, blank=True)
    alt_phone = models.CharField(max_length = 50, blank=True)


    def total(self):
        return self.delivery_fee + self.item_total

    def __str__(self):
        return "(" + str(self.pk) + ") " + self.first_name + " " + self.time.strftime("%d-%m-%Y")

    def num(self):
        return "F{:03d}".format(self.id)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    filament = models.ForeignKey(Filament, on_delete = models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return "Order ID (" + str(self.order.pk) +")"

#class Profile(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    address = models.TextField(max_length = 100, blank=False, null=True)
#    phone = models.CharField(max_length = 50, blank=False, null=True)
#    company = models.CharField(max_length = 100, blank=True, null=True)
#    region = models.ForeignKey(Region, on_delete = models.SET_NULL, null=True, default=1)

#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)
#    instance.profile.save()    