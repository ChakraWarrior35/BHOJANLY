from django.contrib import admin
from home.models import Contact, Restaurant, Delivery, DeliveryPartner
# Register your models here.
admin.site.register(Contact)
admin.site.register(Restaurant)
admin.site.register(Delivery)
admin.site.register(DeliveryPartner)