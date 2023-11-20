from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required


app_name = "ku-market-place"
urlpatterns = [
    path('', RedirectView.as_view(url="product/"), name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('order_list/', login_required(views.order_list, login_url="google_login"), name='order_list'),
    path('product/', views.ProductView.as_view(), name='product'),
    path(
        'single_product/<int:pk>/',
        views.ProductDetailView.as_view(),
        name='single_product'
    ),
    path('cart/', login_required(views.CartDailView.as_view(), login_url="google_login"), name='view_cart'),
    path('add/<int:product_id>/', login_required(views.AddToCartView.as_view(), login_url="google_login"), name='add_to_cart'),
    path('remove/<int:product_id>/', login_required(views.RemoveFromCartView.as_view(), login_url="google_login"), name='remove_from_cart'),
    path('order/<int:order_id>', login_required(views.OrderView.as_view(), login_url="google_login"), name='order'),
]
