"""
URL configuration for pos_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from pos_app import views
from django.urls import path
from pos_app import views
from django.urls import path
from pos_app import views
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('main_menu/', views.main_menu, name='main_menu'),
    path('add_item_menu/', views.add_item_menu, name='add_item_menu'),
    path('view_menu/', views.view_menu, name='view_menu'),
    path('remove_item_menu/', views.remove_item_menu, name='remove_item_menu'),
    path('menu_and_order/', views.menu_and_order, name='menu_and_order'),
    path('generate_receipt/', views.generate_receipt, name='generate_receipt'),
    path('', views.home, name='home'),
    path('inventory_management/', views.inventory_management, name='inventory_management'),
    path('sales_order_analytics/', views.sales_order_analytics, name='sales_order_analytics'),
]
    # Add more URLs for additional views if needed
