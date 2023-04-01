from django.urls import path
from . import views


urlpatterns = [
    path('menu-items/', views.MenuItemViews.as_view({'get': 'list', 'post': 'create'})),
    path('menu-items/<int:pk>/', views.MenuItemViews.as_view({'get': 'retrieve', 'patch': 'update', 'put': 'update', 'delete': 'destroy'})),
    path('groups/manager/users/', views.list_add_managers),
    path('groups/manager/users/<int:userId>/', views.delete_managers),
    path('groups/delivery-crew/users/', views.list_add_delivery_crew),
    path('groups/delivery-crew/users/<int:userId>/', views.delete_delivery_crew),
    path('cart/menu-items/', views.CartViews.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'})),
    path('orders/', views.OrderViews.as_view({'get': 'list'}))
]