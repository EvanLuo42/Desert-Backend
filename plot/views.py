from django.http import JsonResponse

import song
from plot import models
from django.utils.translation import gettext as _

from plot.forms import PlotForm, ChapterForm

Plot = models.Plot
Chapter = models.Chapter
ChapterUnlock = models.ChapterUnlock
PlotRead = models.PlotRead
SongInfo = song.SongInfo
SongUnlock = song.SongUnlock


def dump_plots(plots, plots_read):
    return [{
        'plot_id': plot.plot_id,
        'plot_content': plot.content,
        'plot_title': plot.plot_title,
        'is_read': plots_read.filter(plot_id=plot.plot_id).exists()
    } for plot in plots]


def dump_plot(plot, plots_read):
    return {
        'plot_id': plot.plot_id,
        'plot_content': plot.content,
        'plot_title': plot.plot_title,
        'is_read': plots_read.filter(plot_id=plot.plot_id).exists()
    }


def dump_chapters(chapters, chapters_unlock):
    return [{
        'chapter_id': chapter.chapter_id,
        'chapter_name': chapter.chapter_name,
        'plot_id': chapter.plot_id,
        'is_unlock': chapters_unlock.filter(chapter_id=chapter.chapter_id).exists()
    } for chapter in chapters]


def dump_chapter(chapter, chapters_unlock):
    return {
        'chapter_id': chapter.chapter_id,
        'chapter_name': chapter.chapter_name,
        'plot_id': chapter.plot_id,
        'is_unlock': chapters_unlock.filter(chapter_id=chapter.chapter_id).exists()
    }


def get_all_plots_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_id = request.session.get('user_id')
            plots_read = PlotRead.objects.filter(user_id=user_id)
            return JsonResponse({'status': 'success', 'plots': dump_plots(Plot.objects.all(), plots_read)})
        else:
            return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def get_plot_info_view(request):
    if request.method == 'GET':
        form = PlotForm(request.GET)
        if form.is_valid():
            if request.user.is_authenticated:
                plot_id = form.clean_plot_id()
                user_id = request.session.get('user_id')
                plot = Plot.objects.get(plot_id=plot_id)
                return JsonResponse({'status': 'success',
                                     'plot': dump_plot(plot, PlotRead.objects.filter(user_id=user_id))})
            else:
                return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def get_all_chapter_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_id = request.session.get('user_id')
            chapters = Chapter.objects.all()
            return JsonResponse({'status': 'success',
                                 'chapters': dump_chapters(chapters, ChapterUnlock.objects.filter(user_id=user_id))})
        else:
            return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def get_chapter_info(request):
    if request.method == 'GET':
        form = ChapterForm(request.GET)
        if form.is_valid():
            if request.user.is_authenticated:
                user_id = request.session.get('user_id')
                chapter_id = form.clean_chapter_id()
                chapter = Chapter.objects.filter(chapter_id=chapter_id)
                return JsonResponse({'status': 'success',
                                     'chapters': dump_chapter(chapter,
                                                              ChapterUnlock.objects.filter(user_id=user_id))})
            else:
                return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def read_plot_view(request):
    if request.method == 'POST':
        form = PlotForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                user_id = request.session.get('user_id')
                plot_id = form.clean_plot_id()
                if PlotRead.objects.filter(user_id=user_id, plot_id=plot_id).exists():
                    return JsonResponse({'status': 'error', 'message': _('You have already read this plot')},
                                        status=400)
                else:
                    plot = PlotRead.objects.create(user_id=user_id, plot_id=plot_id)
                    plot.save()
                    song_info = SongInfo.objects.filter(plot_id=plot_id)
                    chapter = Chapter.objects.filter(plot_id=plot_id)
                    if song_info.exists():
                        if SongUnlock.objects.filter(user_id=user_id,
                                                     song_id=song_info.first().song_id):
                            return JsonResponse({'status': 'success',
                                                 'message': _('You have already unlocked this song')}, status=400)
                        else:
                            SongUnlock.objects.create(user_id=user_id, plot_id=plot_id,
                                                      song_id=song_info.first().song_id).save()
                            return JsonResponse({'status': 'success', 'message': _('Read plot successfully')})
                    elif chapter.exists():
                        if ChapterUnlock.objects.filter(user_id=user_id, chapter_id=chapter.first().chapter_id):
                            return JsonResponse({'status': 'error',
                                                 'message': _('You have already unlocked this chapter')}, status=400)
                        else:
                            ChapterUnlock.objects.create(user_id=user_id, plot_id=plot_id,
                                                         chapter_id=chapter.first().chapter_id).save()
                            return JsonResponse({'status': 'success', 'message': _('Read plot successfully')})
                    else:
                        return JsonResponse({'status': 'error',
                                             'message': _('This Plot does not belong to any song or chapter')},
                                            status=400)
            else:
                return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)
