from django.urls import path

from client_stat.views import ClientStatView

app_name = "client_stat"

urlpatterns = [
    path("", ClientStatView.as_view(), name="client_stat")
]
