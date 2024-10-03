from django.contrib import admin

from contracts.models import Contracts

class ContractsAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "date", "start_date",  "end_date", "amount", "manager", "service_provided"
    list_display_links = "pk", "title"


admin.site.register(Contracts, ContractsAdmin)
