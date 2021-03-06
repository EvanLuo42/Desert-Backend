from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

import link.views
import player.views
import plot.views
import song.views

from desert import settings

from django_otp.admin import OTPAdminSite

admin.site.__class__ = OTPAdminSite

urlpatterns = [
    path('login/', player.views.login_view),
    path('register/', player.views.register_view),
    path('captcha/', player.views.send_captcha_view),
    path('password/reset/', player.views.reset_password_view),
    path('logout/', player.views.logout_view),
    path('player/friend/add/', player.views.add_friend_view),
    path('player/friends/get/', player.views.get_friends_view),
    path('players/get/', player.views.get_all_players_view),
    path('player/get/', player.views.get_player_view),
    path('player/roles/get/', player.views.get_all_unlocked_character_view),
    path('player/role/select/', player.views.select_role_view),
    path('player/friend/delete/', player.views.delete_friend_view),
    path('score/post/', song.views.upload_score_view),
    path('score/get/', song.views.get_latest_score_view),
    path('scores/get/', song.views.get_all_scores),
    path('songs/get/', song.views.get_all_songs_info_view),
    path('song/get/', song.views.get_song_info_view),
    path('song/download/', song.views.download_song_file_view),
    path('scores/get/', song.views.get_top_scores_by_song_id_view),
    path('announcement/get/', song.views.announcement_view),
    path('api/version/get/', song.views.get_api_version_view),
    path('plots/get/', plot.views.get_all_plots_view),
    path('plot/get/', plot.views.get_plot_info_view),
    path('chapters/get/', plot.views.get_all_chapters_view),
    path('chapter/get/', plot.views.get_chapter_info_view),
    path('plot/read/', plot.views.read_plot_view),
    path('item/get/', plot.views.get_item_by_id_view),
    path('link/valid/', link.views.is_token_available_view),
    path('link/get/', link.views.get_link_token_view),
    path('link/post/', player.views.view_c178mob_func),
    path('desert/admin/', admin.site.urls),
    re_path('static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

handler404 = player.views.page_not_found
