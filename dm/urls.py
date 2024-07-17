from django.urls import path
from . import views

app_name = 'dm'

urlpatterns = [
    path('dm/', views.dm_page, name='dm_page'), 
]