from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.db import connection
from dm.forms import RoomForm
from dm.models import Room
from django.http import JsonResponse
from subscriptions.models import Subscription
from accounts.models import Player, CustomUser
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
    # with connection.cursor() as cursor:
    #     # 해당 유저(user_id)가 구독한 선수들의 id (player 테이블의 id) 목록
    #     cursor.execute("SELECT subscribed_to_player_id FROM subscriptions_subscription WHERE subscriber_id = %s", [user_id])
    #     be_subscribed_players_ids = [item[0] for item in cursor.fetchall()]

    #     # 선수들의 id(player테이블의 id)로 선수들의 id(player테이블의 id)와 이름을 조회
    #     cursor.execute("SELECT id, player_name FROM accounts_player WHERE id IN %s", [tuple(be_subscribed_players_ids)])
    #     players_id_name = cursor.fetchall() # fetchall의 결과는 튜플의 리스트로 반환되므로 다음과 같이 형변환

    # context = {
    #     'players_list': players_id_name,
    #     'user_id' : user_id
    # }
    # return render(request, 'dm/index.html', context)

    # 현재 로그인한 사용자가 구독한 선수들의 목록을 가져옵니다.
    subscribed_players = Subscription.objects.filter(subscriber=user_id)

    context = {
        'players' : subscribed_players,
        'user_id' : user_id
    }

    return render(request, 'dm/index.html', context)

def player_dm(request: HttpRequest, user_id: str, player_id: str) -> HttpResponse:
    # context = {
    #     'user_id' : user_id,
    #     'player_id': player_id,
    # }
    user = get_object_or_404(CustomUser, id=user_id)
    player = get_object_or_404(Player, id=player_id)
    
    context = {
        'user': user,
        'player': player,
    }
    return render(request, 'dm/room_dm.html', context)

def player_room(request: HttpRequest, user_id: str):
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT id FROM accounts_player WHERE user_id = %s", [user_id])
    #     user_id_to_player_id = str(cursor.fetchall()[0][0])
    # context = {
    #     'user_id' : user_id,
    #     'player_id' : user_id_to_player_id,
    # }
    player = Player.objects.get(user_id=user_id)
    context = {
        'user_id' : user_id,
        'player_id' : player.id,
        'player' : player
    }

    return render(request, 'dm/player_room_dm.html', context)


def load_chat(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    chat_messages = ChatMessage.objects.filter(player=player)
    # 채팅 메시지와 프로필 사진을 HTML로 렌더링
    chat_messages_html = render_to_string('dm/chat_messages.html', {'chat_messages': chat_messages})
    player_image_url = player.image.url
    return JsonResponse({'chat_messages': chat_messages_html, 'player_image': player_image_url})