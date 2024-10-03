from django.urls import path

from ads.views import (
    AdsListView,
    AdsCreateView,
    AdsDetailView,
    AdsEditView,
    AdsDeleteView,
    AdsStatisticView,
)

app_name = "ads"

urlpatterns = [
    path("", AdsListView.as_view(), name="ads_list"),
    path("new/", AdsCreateView.as_view(), name="new_ads"),
    path("<int:pk>/", AdsDetailView.as_view(), name="ads_detail"),
    path("<int:pk>/edit/", AdsEditView.as_view(), name="ads_edit"),
    path("<int:pk>/delete/", AdsDeleteView.as_view(), name="ads_delite"),
    path("statistic/", AdsStatisticView.as_view(), name="ads_statistic"),
]