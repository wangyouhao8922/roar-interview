from django.contrib import admin
from .models import Shows, Locations, ShowInfos ,Units, ShowUnitRoles

admin.site.register([Shows, Locations, ShowInfos ,Units, ShowUnitRoles])