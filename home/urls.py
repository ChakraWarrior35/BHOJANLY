from django.contrib import admin
from django.urls import path, include
from home import views
from . import views
urlpatterns = [
path('', views.index, name='index'),
path('about/', views.about, name='about'),
path('services/', views.services, name='services'),
path('contact/', views.contact, name='contact'),
path('resturent/', views.resturent, name='resturent'),
path('delivery/', views.delivery, name='delivery'), 
path('creat/', views.creat_partner, name='creat_partner'),
path('login/', views.login, name='login'),
path('logout/', views.logout, name='logout'),
path('cart/', views.cart, name='cart'),
path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
path('buy/', views.buy, name='buy'),
]