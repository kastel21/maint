from django.contrib import admin

# Register your models here.
from django.contrib import admin
from vehicle.models import *

admin.site.register(Request)
admin.site.register(Customer)
admin.site.register(Assessments)
admin.site.register(Service)
admin.site.register(Bike)
