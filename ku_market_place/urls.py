from django.urls import path
from . import views
from django.views.generic import RedirectView


app_name = "ku-market-place"
urlpatterns = [
    path('', RedirectView.as_view(url="product/"), name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('order_list/', views.order_list, name='order_list'),
    path('product/', views.ProductView.as_view(), name='product'),
    path(
        'single_product/<int:pk>/',
        views.ProductDetailView.as_view(),
        name='single_product'
    ),
    path('lowest-price', views.ASCProduct.as_view(), name='lowest_price'),
    path('highest-price', views.DESCProduct.as_view(), name='highest_price'),
    path('newest-items', views.NewProduct.as_view(), name='newest_items'),
    path('cart/', views.CartDailView.as_view(), name='view_cart'),
    path('add/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
]
