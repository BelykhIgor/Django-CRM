from django.contrib import admin

from leads.models import Leads


class LeadsAdmin(admin.ModelAdmin):
    list_display = "pk", "first_name", "last_name", "phone_number", "email", "promotion_channel"
    list_display_links = "pk", "first_name", "last_name"

admin.site.register(Leads, LeadsAdmin)