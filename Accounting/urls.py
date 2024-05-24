from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('organization/create/', views.organization_create, name='organization-create'),
    path('organization/create/add-by-inn/<int:pk>/', views.organization_create_by_inn, name='organization-create-by-inn'),
    path('organization/<int:pk>/', views.organization_detail, name='organization-detail'),
    path('organization/<int:pk>/edit/', views.organization_edit, name='organization-edit'),
    path('dogovor/create/', views.dogovor_create, name='dogovor-create'),
    path('dogovor/create/<int:pk>/', views.dogovor_create_target, name='dogovor-create-target'),
    path('dogovor/<int:pk>/', views.dogovor_detail, name='dogovor-detail'),
    path('dogovor/<int:pk>/edit/', views.dogovor_edit, name='dogovor-edit'),
    path('dogovor/<int:pk>/generate/', views.dogovor_generate, name='dogovor-generate'),
    path('service/create/', views.service_create, name='service-create'),
    path('service/<int:pk>/', views.service_detail, name='service-detail'),
    path('service/<int:pk>/edit/', views.service_edit, name='service-edit'),
    path('service/<int:pk>/generate-bill/', views.service_generate_bill, name='service-generate-bill'),
    path('service/<int:pk>/generate-act/', views.service_generate_act, name='service-generate-act'),
]