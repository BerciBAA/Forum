from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginPage, name='loginPage'),
    path('profile/<str:pk>', views.profilePage, name='profilePage'),
    path('register/', views.registerPage, name='registerPage'),
    path('logout/', views.logoutPage, name='logoutPage'),
    path('room/<str:pk>/', views.roomPage, name='roomPage'),
    path('create-room/', views.createRoom, name='createRoom'),
    path('create-topic/', views.createTopic, name='createTopic'),
    path('delete-room/<str:pk>', views.deleteRoom, name='deleteRoom')
    
]
