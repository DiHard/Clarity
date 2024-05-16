from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('organization/create/', views.organization_create, name='organization-create'),
    path('organization/<int:pk>/', views.organization_detail, name='organization-detail'),
    path('organization/<int:pk>/edit/', views.organization_edit, name='organization-edit'),
    path('dogovor/<int:pk>/', views.dogovor_detail, name='dogovor-detail'),
    path('dogovor/<int:pk>/edit/', views.dogovor_edit, name='dogovor-edit'),
    path('dogovor/<int:pk>/generate/', views.dogovor_generate, name='dogovor-generate'),
    path('service/<int:pk>/', views.service_detail, name='service-detail'),
]