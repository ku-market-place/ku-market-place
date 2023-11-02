from django.urls import path
from ku_market_place.views import HomePageView
from . import views


app_name = "ku-market-place"
urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('order_list/', views.order_list, name='order_list'),
    path('product/', views.ProductView.as_view(), name='product'),
    path('single_product/', views.single_product, name='single_product'),
]
