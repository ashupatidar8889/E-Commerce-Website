from django.urls import path
from . import views

urlpatterns = [
    # HOME + PRODUCTS
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),

    # CART
    path('cart/', views.cart, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('inc/<int:product_id>/', views.increase_quantity, name='inc'),
    path('dec/<int:product_id>/', views.decrease_quantity, name='dec'),

    # ORDER
    path('checkout/', views.checkout, name='checkout'),

    # AUTH
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
]