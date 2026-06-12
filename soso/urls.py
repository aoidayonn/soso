from django.urls import path
from . import views

app_name = "soso"

urlpatterns = [
    path("main/", views.TopPage.as_view(), name="top_page"),
    path("login/", views.UserLogin.as_view(), name="user_login"),
    path("registerUser/", views.UserCreate.as_view(), name="user_create"),
    path("registerUserConfirm/", views.UserCreateConfirm.as_view(), name="user_confirm"),
    path("userInfo/", views.UserInfo.as_view(), name="user_info"),
    path('logout/', views.UserLogout.as_view(), name='user_logout'),
]
