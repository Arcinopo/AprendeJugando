from django.urls import path
from .views import CustomLoginView, CustomLogoutView, register_view, verify_email_view

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path('verify/', verify_email_view, name='verify_email'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]