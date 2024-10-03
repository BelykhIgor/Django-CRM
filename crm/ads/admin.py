from django.contrib import admin

from ads.models import Ads


class AdsAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "promotion_channel", "advertising_budget"
    list_display_links = "pk", "title"

admin.site.register(Ads, AdsAdmin)