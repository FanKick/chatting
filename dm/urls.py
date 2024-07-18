from django.urls import path
from dm import views

app_name = 'dm'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_pk>/dm/', views.room_dm, name='room_dm'),
    path('new/', views.room_new, name='room_new'),
]