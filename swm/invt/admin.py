from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
admin.site.register(TUser)
admin.site.register(Waste)
admin.site.register(ProcesssingPlant)
admin.site.register(TransportVehicle)
admin.site.register(Landfill)

@admin.register(WasteML)
class WasteMLAdmin(ImportExportModelAdmin):
    pass


