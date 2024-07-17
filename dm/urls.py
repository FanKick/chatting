from django.urls import path
from dm import views

app_name = 'dm'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/dm/', views.room_dm, name='room_dm'),
]