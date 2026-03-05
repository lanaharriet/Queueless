from django.urls import path
from . import views

urlpatterns = [
    path("", views.menu_page, name="menu"),
    path("confirm/", views.confirm_order, name="confirm"),
    path("order/", views.place_order, name="order"),
    path('token/<int:order_id>/', views.download_token, name='download_token'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard-login/', views.dashboard_login, name='dashboard_login'),
]