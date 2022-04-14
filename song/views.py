from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _

from desert import settings, constant
from song import models
from song.forms import UploadScoreForm, GetSongInfoForm
from song.models import Announcement

SongRecord = models.SongRecord
SongInfo = models.SongInfo
SongUnlock = models.SongUnlock
User = get_user_model()


def songs_dump(songs, songs_unlock):
    return [{
        'song_id': song.song_id,
        'song_name': song.song_name,
        'song_author': song.song_author,
        'score_author': song.score_author,
        'difficulty': song.difficulty,
        'image_url': song.image_file.url,
        'level': song.level,
        'file_md5': song.file_md5,
        'is_lock': songs_unlock.filter(song_id=song.song_id).exists(),
    } for song in songs]


def song_dump(song, songs_unlock):
    return {
        'song_id': song.song_id,
        'song_name': song.song_name,
        'song_author': song.song_author,
        'score_author': song.score_author,
        'difficulty': song.difficulty,
        'image_url': song.image_file.url,
        'level': song.level,
        'is_lock': songs_unlock.filter(song_id=song.song_id).exists(),
        'file_md5': song.file_md5,
    }


def score_dump(score):
    return {
        'song_id': score.song_id,
        'user_id': score.user_id,
        'score': score.score,
        'best_score': score.best_score,
        'created_at': score.created_at,
    }


def scores_dump(scores):
    return [{
        'song_id': score.song_id,
        'user_id': score.user_id,
        'score': score.score,
        'best_score': score.best_score,
        'created_at': score.created_at,
    } for score in scores]


def announcement_dump(announcement):
    return {
        'announcement_id': announcement.announcement_id,
        'content': announcement.content,
    }


@csrf_exempt
def upload_score_view(request):
    if request.method == constant.POST_METHOD:
        form = UploadScoreForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                user_id = request.session.get('user_id')
                song_id = form.clean_song_id()
                score = form.cleaned_data.get('score')
                rank_point = form.cleaned_data.get('rank_point')

                if SongRecord.objects.filter(user_id=user_id, song_id=song_id).exists():
                    if SongRecord.objects.get(user_id=user_id, song_id=song_id).best_score < score:
                        SongRecord.objects.update(user_id=user_id, song_id=song_id, score=score,
                                                  best_score=score)
                    else:
                        SongRecord.objects.update(user_id=user_id, song_id=song_id, score=score)
                else:
                    SongRecord.objects.create(user_id=user_id, song_id=song_id, score=score,
                                              best_score=score)

                User.objects.filter(user_id=user_id).update(rank_point=rank_point)

                return JsonResponse({'status': 'success', 'message': _('Score uploaded successfully')})
            else:
                return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def get_all_songs_info_view(request):
    if request.method == constant.GET_METHOD:
        if request.user.is_authenticated:
            songs = SongInfo.objects.all()
            user_id = request.session.get('user_id')
            songs_unlock = SongUnlock.objects.filter(user_id=user_id)
            return JsonResponse({'status': 'success', 'songs': songs_dump(songs, songs_unlock)})
        else:
            return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def get_song_info_view(request):
    if request.method == constant.GET_METHOD:
        form = GetSongInfoForm(request.GET)
        if form.is_valid():
            if request.user.is_authenticated:
                user_id = request.session.get('user_id')
                return JsonResponse({'status': 'success', 'song': song_dump(
                    SongInfo.objects.filter(song_id=form.clean_song_id()).first(),
                    SongUnlock.objects.filter(user_id=user_id))})
            else:
                return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def download_song_file_view(request):
    if request.method == constant.GET_METHOD:
        form = GetSongInfoForm(request.GET)
        if form.is_valid():
            song_id = form.clean_song_id()
            song_url = SongInfo.objects.filter(song_id=song_id).first().song_file.url
            return redirect(song_url)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def get_latest_score_view(request):
    if request.method == constant.GET_METHOD:
        if request.user.is_authenticated:
            user_id = request.session.get('user_id')
            if SongRecord.objects.filter(user_id=user_id).exists():
                score = SongRecord.objects.filter(user_id=user_id).order_by('-created_at').first()
                return JsonResponse({'status': 'success', 'score': score_dump(score)})
            else:
                return JsonResponse({'status': 'error', 'message': _('No score')}, status=404)
        else:
            return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def get_all_scores(request):
    if request.method == constant.GET_METHOD:
        if request.user.is_authenticated:
            user_id = request.session.get('user_id')
            scores = SongRecord.objects.filter(user_id=user_id)
            return JsonResponse({'status': 'success', 'scores': scores_dump(scores)})
        else:
            return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def get_top_scores_by_song_id_view(request):
    if request.method == constant.GET_METHOD:
        form = GetSongInfoForm(request.GET)
        if form.is_valid():
            song_id = form.clean_song_id()
            scores = SongRecord.objects.filter(song_id=song_id).order_by('-score')[:10]
            return JsonResponse({'status': 'success', 'scores': scores_dump(scores)})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def announcement_view(request):
    if request.method == constant.GET_METHOD:
        if Announcement.objects.exists():
            announcement = Announcement.objects.order_by('-created_at').first()
            return JsonResponse({'status': 'success', 'announcement': announcement_dump(announcement)})
        else:
            return JsonResponse({'status': 'success', 'content': None})
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def get_api_version_view(request):
    if request.method == constant.GET_METHOD:
        return JsonResponse({'status': 'success', 'version': settings.API_VERSION})
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)
