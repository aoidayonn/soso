from django.urls import path
from . import views

app_name = "soso"

urlpatterns = [
    path("", views.IndexView.as_view()),
    path("top/", views.IndexView.as_view(), name="top_page"),
]
