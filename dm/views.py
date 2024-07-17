from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.
def dm_page(request):
    return render(request, 'dm/dm_page.html')

def index(request):
    return render(request, 'dm/index.html')

def room_dm(request: HttpRequest, room_name: str) -> HttpResponse:
    context = {
        'room_name': room_name,
    }
    return render(request, 'dm/room_dm.html', context)