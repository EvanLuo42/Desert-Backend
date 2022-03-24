"""mvgbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import player.views
import song.views

urlpatterns = [
    path('login/', player.views.login_view),
    path('register/', player.views.register_view),
    path('add_friend/', player.views.add_friend_view),
    path('get_friends/', player.views.get_friends_view),
    path('get_all_players/', player.views.get_all_players_view),
    path('get_player/', player.views.get_player_view),
    path('delete_friend/', player.views.delete_friend_view),
    path('upload_score/', song.views.upload_score_view),
    path('get_all_songs/', song.views.get_all_songs_info_view),
    path('get_song/', song.views.get_song_info_view),
    path('download_song/', song.views.download_song_file_view),
    path('admin/', admin.site.urls),
]
