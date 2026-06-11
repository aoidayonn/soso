from django.urls import path
from . import views

app_name = "soso"

urlpatterns = [
    path("login/", views.UserLogin.as_view(), name="user_login"),
    path("registerUser/", views.UserCreate.as_view(), name="user_create"),
    path("registerUserConfirm/", views.UserCreateConfirm.as_view(), name="user_confirm"),
]
