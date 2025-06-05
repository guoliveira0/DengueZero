from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('create/', views.create_report, name='create_report'),
    path('success/', views.report_success, name='report_success'),
    path('change_status/<int:report_id>/', views.change_status, name='change_status'),
    path('login/', views.custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('api/dengue_heatmap/', views.dengue_heatmap, name='dengue_heatmap'),
    path('informacoes-dengue/', views.dengue_info, name='dengue_info'),  # Nova URL
]

# Adicionar isto no final do arquivo - crucial para servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)