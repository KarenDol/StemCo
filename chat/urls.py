from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('new_chat/', views.new_chat, name='new_chat'),
    path('image/', views.image, name='image'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout'),
]