from django.urls import path
from . import views_auth, views_user, views_owner , views_chat

urlpatterns = [
    # --- Authentication ---
    path('', views_auth.login_user, name='login'),
    path('login/', views_auth.login_user, name='login'),
    path('logout/', views_auth.logout_user, name='logout'),
    path('register/', views_auth.register_user, name='register'),

    # --- User Routes ---
    path('user/dashboard/', views_user.user_dashboard, name='user_dashboard'),
    path('user/profile/', views_user.user_profile, name='user_profile'),
    path('profile/create/', views_user.create_profile, name='create_profile'),

    path('user/preferences/', views_user.user_preferences, name='user_preferences'),
    path('user/find-roommates/', views_user.find_roommates, name='find_roommates'),
    path('user/rate-room/<int:room_id>/', views_user.rate_room, name='rate_room'),

    # --- Owner Routes ---
    path('owner/dashboard/', views_owner.owner_dashboard, name='owner_dashboard'),
    path('rooms/add/', views_owner.add_room, name='add_room'),
    path('rooms/<int:pk>/edit/', views_owner.edit_room, name='edit_room'),
    path('rooms/<int:pk>/delete/', views_owner.delete_room, name='delete_room'),
    path('owner-profile/', views_owner.owner_profile_complete, name='owner_profile_complete'),
    path('owner/profile/', views_owner.owner_profile, name='owner_profile'),
    path('owner/profile/edit/', views_owner.edit_owner_profile, name='edit_owner_profile'),

    
    


    path('start/<int:room_id>/', views_chat.start_chat, name='start_chat'),
    path('room/<int:chat_id>/', views_chat.chat_room, name='chat_room'),
 
    path('owner/chats/', views_chat.owner_chat_list, name='owner_chat_list'),
    path('user/chats/', views_chat.user_chat_list, name='user_chat_list'),
    path('start-user-chat/<int:user_id>/', views_chat.start_user_chat, name='start_user_chat'),

]
