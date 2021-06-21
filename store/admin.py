#admin files for the store

from django.contrib import admin
from store.models import Filament, Brand, Material, Order, OrderDetail

admin.site.register(Filament)
admin.site.register(Brand)
admin.site.register(Material)
admin.site.register(Order)
admin.site.register(OrderDetail)
#admin.site.register(Profile)
