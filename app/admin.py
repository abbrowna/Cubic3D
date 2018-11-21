from django.contrib import admin

from .models import PrintRequest,ThingOrders,Profile,Quote,Material,Invoice,GroupRecord

admin.site.register(PrintRequest)
admin.site.register(ThingOrders)
admin.site.register(Profile)
admin.site.register(Quote)
admin.site.register(Material)
admin.site.register(Invoice)
admin.site.register(GroupRecord)