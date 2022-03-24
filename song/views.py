from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

from song import models
from song.forms import UploadScoreForm, GetSongInfoForm

SongRecord = models.SongRecord
SongInfo = models.SongInfo


def songs_dump(songs):
    return [{
        'song_id': song.song_id,
        'song_name': song.song_name,
        'song_author': song.song_author,
        'score_author': song.score_author,
        'difficulty': song.difficulty,
        'level': song.level,
    } for song in songs]


def song_dump(song):
    return {
        'song_id': song.song_id,
        'song_name': song.song_name,
        'song_author': song.song_author,
        'score_author': song.score_author,
        'difficulty': song.difficulty,
        'level': song.level,
    }


@csrf_exempt
def upload_score_view(request):
    if request.method == 'POST':
        form = UploadScoreForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            user_id = request.session.get('user_id')
            song_id = form.clean_song_id()
            score = form.cleaned_data.get('score')
            song_record = SongRecord.objects.create(user_id=user_id, song_id=song_id, score=score)
            song_record.save()

            return JsonResponse({'status': 'success', 'message': 'Score uploaded successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@csrf_exempt
def get_all_songs_info_view(request):
    if request.method == 'GET':
        songs = SongInfo.objects.all()
        return JsonResponse({'status': 'success', 'songs': songs_dump(songs)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@csrf_exempt
def get_song_info_view(request):
    if request.method == 'GET':
        form = GetSongInfoForm(request.GET)
        if form.is_valid():
            return JsonResponse({'status': 'success', 'message': song_dump(
                SongInfo.objects.filter(song_id=form.clean_song_id()).first())})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@csrf_exempt
def download_song_file_view(request):
    if request.method == 'GET':
        form = GetSongInfoForm(request.GET)
        if form.is_valid():
            song_id = form.clean_song_id()
            song_file = SongInfo.objects.filter(song_id=song_id).first().song_file.file
            response = StreamingHttpResponse(song_file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(song_file.name)
            return response
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
