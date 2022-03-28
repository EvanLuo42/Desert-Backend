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
    path('get_latest_score/', song.views.get_latest_score_view),
    path('get_top_scores/', song.views.get_top_scores_by_song_id_view),
    path('admin/', admin.site.urls),
]
