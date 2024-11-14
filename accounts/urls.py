from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .views import register, login_view, logout_view, profile_view, delete_user_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('delete/', delete_user_view, name='delete'),
]
