from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.db import connection
from dm.forms import RoomForm
from dm.models import Room

# Create your views here.
def dm_page(request):
    return render(request, 'dm/dm_page.html')
# index 함수에선 받아온 해싱된 id값을 
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
# user_id를 통한 구독 선수 목록 리스트
def be_subscribed_players_index(request, user_id):
    with connection.cursor() as cursor:
        # 해당 유저(user_id)가 구독한 선수들의 id 목록
        cursor.execute("SELECT subscribed_to_player_id FROM subscriptions_subscription WHERE subscriber_id = %s", [user_id])
        be_subscribed_players_ids = [item[0] for item in cursor.fetchall()]

        # 선수들의 id로 선수들의 id와 이름을 조회
        cursor.execute("SELECT id, player_name FROM accounts_player WHERE id IN %s", [tuple(be_subscribed_players_ids)])
        players_id_name = cursor.fetchall() # fetchall의 결과는 튜플의 리스트로 반환되므로 다음과 같이 형변환

    context = {
        'players_list': players_id_name,
        'user_id' : user_id
    }
    return render(request, 'dm/index.html', context)

def player_dm(request: HttpRequest, user_id: str, player_id: str) -> HttpResponse:
    context = {
        'user_id' : user_id,
        'player_id': player_id,
    }
    return render(request, 'dm/room_dm.html', context)