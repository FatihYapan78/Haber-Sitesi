from django.contrib import admin
from django.urls import path
from AppHaber.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("haber_site/<slug:haber_site>", category, name="haber_site"),
    path("haber_site/<slug:haber_site>/kategori/<slug:category>/", subcategory, name="subcategory"),
]
