from django.urls import path

from customers.views import (
    CustomersListView,
    CreateCustomersView,
    CustomersDetailView,
    CustomersEditView,
    CustomersDeleteView
)

app_name = "customers"

urlpatterns = [
    path("", CustomersListView.as_view(), name="customers_list"),
    path("new/", CreateCustomersView.as_view(), name="customers_create"),
    path("<int:pk>/", CustomersDetailView.as_view(), name="customers_detail"),
    path("<int:pk>/edit/", CustomersEditView.as_view(), name="customers_edit"),
    path("<int:pk>/delete/", CustomersDeleteView.as_view(), name="customers_delete"),
]