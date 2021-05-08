#admin files for the store

from django.contrib import admin
from store.models import Filament, Brand, Material, Region, Order, OrderDetail
from app.models import Profile

admin.site.register(Filament)
admin.site.register(Brand)
admin.site.register(Material)
admin.site.register(Region)
admin.site.register(Order)
admin.site.register(OrderDetail)
#admin.site.register(Profile)
