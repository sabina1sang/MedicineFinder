from django.urls import path
from . import views
from .views import add_medicine

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_view, name='search'),
    path('dashboard/user/', views.user_dashboard_view, name='user_dashboard'),
    path('dashboard/pharmacy/', views.pharmacy_dashboard_view, name='pharmacy_dashboard'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('pharmacy/add-medicine/', views.add_medicine, name='add_medicine'),
    path('pharmacy/manage-inventory', views.inv, name='inv'),
    path("edit/<int:pk>/", views.edit_medicine, name="edit_medicine"),
    path("delete/<int:pk>/", views.delete_medicine, name="delete_medicine"),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
     path('map/', views.map_view, name='map'),
    path('api/pharmacies/', views.PharmacyListAPI.as_view(), name='pharmacy_list_api'),
]
