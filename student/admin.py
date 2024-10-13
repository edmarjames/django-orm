from django.contrib import admin

from . import models

admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.Manufacturer)
admin.site.register(models.Warranty)