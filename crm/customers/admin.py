from django.contrib import admin

from customers.models import Customers


class CustomersAdmin(admin.ModelAdmin):
    list_display = "pk", "lead", "get_phone_number", "contract", "get_contract_start_date", "get_contract_end_date"
    list_display_links = "pk", "lead", "contract"

    def get_phone_number(self, obj):
        return obj.lead.phone_number
    get_phone_number.short_description = "Номер телефона"

    def get_contract_end_date(self, obj):
        return obj.contract.end_date
    get_contract_end_date.short_description = "Дата окончания контракта"

    def get_contract_start_date(self, obj):
        return obj.contract.start_date
    get_contract_start_date.short_description = "Дата начала контракта"

admin.site.register(Customers, CustomersAdmin)