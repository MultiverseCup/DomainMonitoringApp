from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.domain_list, name='domain_list'),
    path('add/', views.add_domain, name='add_domain'),
    path('login/', auth_views.LoginView.as_view(template_name='domains/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('domains/<int:pk>/delete/', views.delete_domain, name='delete_domain'),
]