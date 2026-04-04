from django.urls import path
from . import views

urlpatterns = [
    path("", views.menu_page, name="menu"),
    path("confirm/", views.confirm_order, name="confirm"),
    path("order/", views.place_order, name="order"),
    path('token/<int:order_id>/', views.download_token, name='download_token'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard-login/', views.dashboard_login, name='dashboard_login'),
    path("kitchen-control/", views.kitchen_control, name="kitchen_control"),
    path("toggle-item/<int:item_id>/", views.toggle_item, name="toggle_item"),
    path("reset-orders/", views.reset_orders, name="reset_orders"),
    
]