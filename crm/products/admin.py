from django.contrib import admin

from products.models import Products

class ProductsAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "description_short", "price"
    list_display_links = "pk", "title"
    ordering = "pk", "title"
    search_fields = "title", "price"

    def description_short(self, obj):
        return obj.description_short
    description_short.short_description = "Описание"


admin.site.register(Products, ProductsAdmin)
