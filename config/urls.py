from django.contrib import admin
from django.urls import path, include
from soso import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("soso/", include("soso.urls")),
]