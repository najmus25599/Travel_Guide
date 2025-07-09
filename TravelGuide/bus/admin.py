from django.contrib import admin

from .models import Buses, Schedule,Book


admin.site.register(Buses)
admin.site.register(Schedule)
admin.site.register(Book)
# Register your models here.
