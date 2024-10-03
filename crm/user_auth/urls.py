from django.urls import path
from .views import AuthView, LogoutView

app_name = "user_auth"

urlpatterns = [
    path("login/", AuthView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout")
]