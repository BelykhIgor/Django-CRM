from leads.views import (
    LeadsListView,
    CreateLeadsView,
    DetailLeadsView,
    UpdateLeadsView,
    DeleteLeadsView
)
from django.urls import path

app_name = "leads"

urlpatterns = [
    path("", LeadsListView.as_view(), name="leads_list"),
    path("new/", CreateLeadsView.as_view(), name="new_leads"),
    path("<int:pk>/", DetailLeadsView.as_view(), name="detail_leads"),
    path("<int:pk>/edit/", UpdateLeadsView.as_view(), name="edit_leads"),
    path("<int:pk>/delete/", DeleteLeadsView.as_view(), name="delete_leads"),
]