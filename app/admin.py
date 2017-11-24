from django.contrib import admin

from .models import Tempthings,ThingOrders,Profile,Quote

admin.site.register(Tempthings)
admin.site.register(ThingOrders)
admin.site.register(Profile)
admin.site.register(Quote)
