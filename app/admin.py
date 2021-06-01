from django.contrib import admin

from .models import PrintRequest,ThingOrders,Profile,Quote,Material,Invoice,GroupRecord,Region

admin.site.register(PrintRequest)
admin.site.register(ThingOrders)
admin.site.register(Profile)
admin.site.register(Quote)
admin.site.register(Material)
admin.site.register(Invoice)
admin.site.register(GroupRecord)
admin.site.register(Region)