from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # Home Page
    path('login/', views.login_view, name='login'),  # Login Page
    path('logout/', views.logout_view, name='logout'),  # Logout Page
    path('register/', views.register, name='register'),  # Register Page
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard
    path('teams/', views.list_teams, name='teams'),  # Team Management
    path('player/<int:player_id>/', views.player_profile, name='player_profile'),  # Player Profile
    path('payments/', views.payments, name='payments'),  # Payments Page
    path('fines/', views.fines, name='fines'),  # Fines Management
    
    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]