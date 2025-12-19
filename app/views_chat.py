from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Room_Details , Custom_User , ChatMessage


@login_required
def start_chat(request, room_id):
    room = get_object_or_404(Room_Details, id=room_id)
    owner_user = room.owner.user  # assuming your Room_Details has a related owner

    # Check if a chat already exists between the current user and owner for this room
    chat = ChatRoom.objects.filter(room=room)\
                           .filter(participants=request.user)\
                           .filter(participants=owner_user)\
                           .first()

    if not chat:
        chat = ChatRoom.objects.create(room=room)
        chat.participants.add(request.user, owner_user)

    return redirect('chat_room', chat.id)



from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
@require_POST
def send_message(request, chat_id):
    chat = get_object_or_404(ChatRoom, id=chat_id)

    # Ensure user is part of the chat
    if request.user not in chat.participants.all():
        return JsonResponse({'status': 'error', 'msg': 'Unauthorized'}, status=403)

    message_text = request.POST.get('message', '').strip()
    if message_text:
        ChatMessage.objects.create(
            chat=chat,
            sender=request.user,
            message=message_text
        )

    return JsonResponse({'status': 'success'})



@login_required
def chat_room(request, chat_id):
    chat = get_object_or_404(ChatRoom, id=chat_id)

    # Mark unread messages as read
    chat.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    return render(request, 'private_chat.html', {
        'chat': chat,
        'messages': chat.messages.order_by('timestamp')
    })




@login_required
def owner_chat_list(request):
    chats = ChatRoom.objects.filter(participants=request.user)

    chat_data = []
    for chat in chats:
        other_participants = chat.participants.exclude(id=request.user.id)
        chat_data.append({
            'chat': chat,
            'other_participants': other_participants,
            'unread': chat.messages.filter(is_read=False)
                        .exclude(sender=request.user).count(),
            'last': chat.messages.order_by('-timestamp').first()
        })

    return render(request, 'owner_chat_list.html', {
        'chat_data': chat_data
    })



@login_required
def user_chat_list(request):
    chats = ChatRoom.objects.filter(participants=request.user)

    chat_data = []
    for chat in chats:
        # For displaying the other participant(s)
        other_participants = chat.participants.exclude(id=request.user.id)
        chat_data.append({
            'chat': chat,
            'other_participants': other_participants,
            'unread': chat.messages.filter(is_read=False)
                        .exclude(sender=request.user).count(),
            'last': chat.messages.order_by('-timestamp').first()
        })

    return render(request, 'user_chat_list.html', {
        'chat_data': chat_data
    })

from django.db.models import Count


@login_required
def start_user_chat(request, user_id):
    other_user = get_object_or_404(Custom_User, id=user_id)

    # Check if a 1-to-1 chat already exists
    chat = ChatRoom.objects.filter(participants=request.user)\
                           .filter(participants=other_user)\
                           .annotate(num_participants=Count('participants'))\
                           .filter(num_participants=2)\
                           .first()

    if not chat:
        chat = ChatRoom.objects.create()
        chat.participants.add(request.user, other_user)

    return redirect('chat_room', chat.id)


    