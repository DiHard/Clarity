from django.contrib import admin

from .models import Service, Dogovor, Service_type, Organization

# Register your models here.
admin.site.register(Organization)
admin.site.register(Service_type)
admin.site.register(Dogovor)
admin.site.register(Service)