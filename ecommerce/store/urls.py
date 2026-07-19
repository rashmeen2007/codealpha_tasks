from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),

    path('product/', views.product_detail, name='product'),

    path('register/', views.register, name='register'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('cart/', views.cart, name='cart'),

    path('order/', views.order, name='order'),
    path('history/', views.order_history, name='history'),
    path('product/shoes/', views.shoes),

    path('product/headphones/', views.headphones),

    path('product/watch/', views.watch),

    path('product/backpack/', views.backpack),
]
