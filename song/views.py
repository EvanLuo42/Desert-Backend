from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from song import models
from song.forms import UploadScoreForm, GetSongInfoForm
from song.models import Announcement

SongRecord = models.SongRecord
SongInfo = models.SongInfo
User = get_user_model()


def songs_dump(songs):
    return [{
        'song_id': song.song_id,
        'song_name': song.song_name,
        'song_author': song.song_author,
        'score_author': song.score_author,
        'difficulty': song.difficulty,
        'level': song.level,
        'file_md5': song.file_md5,
    } for song in songs]


def song_dump(song):
    return {
        'song_id': song.song_id,
        'song_name': song.song_name,
        'song_author': song.song_author,
        'score_author': song.score_author,
        'difficulty': song.difficulty,
        'level': song.level,
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
    if request.method == 'POST':
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

                return JsonResponse({'status': 'success', 'message': 'Score uploaded successfully'})
            else:
                return JsonResponse({'status': 'error', 'message': 'You have to login first'}, status=401)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)


def get_all_songs_info_view(request):
    if request.method == 'GET':
        songs = SongInfo.objects.all()
        return JsonResponse({'status': 'success', 'songs': songs_dump(songs)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)


def get_song_info_view(request):
    if request.method == 'GET':
        form = GetSongInfoForm(request.GET)
        if form.is_valid():
            return JsonResponse({'status': 'success', 'song': song_dump(
                SongInfo.objects.filter(song_id=form.clean_song_id()).first())})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)


def download_song_file_view(request):
    if request.method == 'GET':
        form = GetSongInfoForm(request.GET)
        if form.is_valid():
            song_id = form.clean_song_id()
            song_url = SongInfo.objects.filter(song_id=song_id).first().song_file.url
            return redirect(song_url)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)


def get_latest_score_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_id = request.session.get('user_id')
            if SongRecord.objects.filter(user_id=user_id).exists():
                score = SongRecord.objects.filter(user_id=user_id).order_by('-created_at').first()
                return JsonResponse({'status': 'success', 'score': score_dump(score)})
            else:
                return JsonResponse({'status': 'error', 'message': 'No score'}, status=404)
        else:
            return JsonResponse({'status': 'error', 'message': 'You have not logged in yet'}, status=401)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)


def get_top_scores_by_song_id_view(request):
    if request.method == 'GET':
        form = GetSongInfoForm(request.GET)
        if form.is_valid():
            song_id = form.clean_song_id()
            scores = SongRecord.objects.filter(song_id=song_id).order_by('-score')[:10]
            return JsonResponse({'status': 'success', 'scores': scores_dump(scores)})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)


def announcement_view(request):
    if request.method == 'GET':
        announcement = Announcement.objects.order_by('-created_at').first()
        return JsonResponse({'status': 'success', 'announcement': announcement_dump(announcement)})
