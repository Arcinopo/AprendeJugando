from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('abecedario/', views.alphabet_view, name='alphabet'),
    path('pizarra/', views.canvas_view, name='canvas'),
    path('pizarra/guardar/', views.save_drawing_api, name='save_drawing'),
    path('cuadernillos/', views.workbook_list_view, name='workbook_list'),
    path('actividad/<int:activity_id>/', views.activity_detail_view, name='activity_detail'),
    path('actividad/<int:activity_id>/verificar/', views.check_activity_api, name='check_activity'),
]