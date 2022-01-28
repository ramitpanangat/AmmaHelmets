from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.homePage, name="home"),
    path("product/<str:id>", views.productDetails, name="productDetails"),
    path("style/<str:style>", views.stylePage, name="stylePage"),
    path("brand/<str:brand>", views.brandPage, name="brandPage"),
    path("results", views.searchProduct, name="search"),
]