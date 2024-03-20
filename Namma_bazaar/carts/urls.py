from django.urls import path,include
from carts import views

urlpatterns = [
    path('', views.cart_page, name='cart_page'),
    path('add-cart/<int:product_id>/', views.add_cart, name='add-cart'),
    path('remove-cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove-cart'),
    path('remove-cart-item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove-cart-item'),
    ]
