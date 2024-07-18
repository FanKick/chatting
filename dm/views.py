from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from dm.forms import RoomForm
from dm.models import Room

# Create your views here.
def dm_page(request):
    return render(request, 'dm/dm_page.html')

def index(request: HttpRequest) -> HttpResponse:
    room_qs = Room.objects.all()
    context = {
        'room_list': room_qs,
    }
    return render(request, 'dm/index.html', context)

def room_dm(request: HttpRequest, room_pk: str) -> HttpResponse:
    room = get_object_or_404(Room, pk=room_pk)
    context = {
        'room': room,
    }
    return render(request, 'dm/room_dm.html', context)

def room_new(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            created_room = form.save()
            return redirect("dm:room_dm", created_room.pk)
    else:
        form = RoomForm()
    return render(request, "dm/room_form.html", {
        "form": form,
    })