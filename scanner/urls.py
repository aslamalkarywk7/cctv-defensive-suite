from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('run-advanced-scan/', views.run_advanced_scan, name='run_advanced_scan'),
    path('run-range-scan/', views.run_range_scan, name='run_range_scan'),
    path('get-history/', views.get_history, name='get_history'),
    path('export-pdf/', views.export_pdf, name='export_pdf'),
    path('export-excel/', views.export_excel, name='export_excel'),
    path('clear-history/', views.clear_history, name='clear_history'),
    path('silent-radar/', views.run_silent_radar, name='silent_radar'),
    path('local-radar/', views.run_local_radar, name='local_radar'),
]
