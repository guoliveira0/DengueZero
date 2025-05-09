from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_report, name='create_report'),
    path('success/', views.report_success, name='report_success'),
    path('change_status/<int:report_id>/', views.change_status, name='change_status'),
]