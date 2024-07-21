from django.urls import path
from dm import views

app_name = 'dm'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:user_id>/', views.be_subscribed_players_index, name='be_subscribed_players_index'),
    path('<str:user_id>/<str:player_id>/dm', views.player_dm, name='player_dm'),
    #path('<str:room_pk>/dm/', views.room_dm, name='room_dm'),
    path('new/', views.room_new, name='room_new'),
]