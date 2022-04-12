from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import song.models as song_models
from plot import models as plot_models
from django.utils.translation import gettext as _

from plot.forms import PlotForm, ChapterForm, ItemForm

Plot = plot_models.Plot
Chapter = plot_models.Chapter
ChapterUnlock = plot_models.ChapterUnlock
PlotRead = plot_models.PlotRead
SongInfo = song_models.SongInfo
SongUnlock = song_models.SongUnlock
Item = plot_models.Item
CharacterUnlock = plot_models.CharacterUnlock


def dump_plots(plots, plots_read):
    return [{
        'plot_id': plot.plot_id,
        'plot_content': plot.plot_content,
        'plot_title': plot.plot_title,
        'is_read': plots_read.filter(plot_id=plot.plot_id).exists()
    } for plot in plots]


def dump_plot(plot, plots_read):
    return {
        'plot_id': plot.plot_id,
        'plot_content': plot.plot_content,
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


def get_all_chapters_view(request):
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


def get_chapter_info_view(request):
    if request.method == 'GET':
        form = ChapterForm(request.GET)
        if form.is_valid():
            if request.user.is_authenticated:
                user_id = request.session.get('user_id')
                chapter_id = form.clean_chapter_id()
                chapter = Chapter.objects.filter(chapter_id=chapter_id).first()
                return JsonResponse({'status': 'success',
                                     'chapters': dump_chapter(chapter,
                                                              ChapterUnlock.objects.filter(user_id=user_id))})
            else:
                return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def get_item_by_id_view(request):
    if request.method == 'GET':
        form = ItemForm(request.GET)
        if form.is_valid():
            if request.user.is_authenticated:
                user_id = request.session.get('user_id')
                item_id = form.clean_item_id()
                item = Item.objects.filter(item_id=item_id).first()
                if item.item_name.startswith('character_'):
                    character_id = int(item.item_name.split('_')[1])
                    if CharacterUnlock.objects.filter(character_id=character_id).exists():
                        return JsonResponse({'status': 'error',
                                             'message': _('You have already unlocked this character, '
                                                          'you can contact us by email to get another one')})
                    else:
                        CharacterUnlock.objects.create(user_id=user_id, character_id=character_id).save()
                        Item.objects.filter(item_id=item_id).delete()
                        return JsonResponse({'status': 'success', 'message': _('Character unlocked')})
                else:
                    return JsonResponse({'status': 'error', 'message': _('Invalid item')})
            else:
                return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


@csrf_exempt
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
                elif plot_id == 1 or PlotRead.objects.filter(user_id=user_id, plot_id=plot_id - 1).exists():
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
                            SongUnlock.objects.create(user_id=user_id,
                                                      song_id=song_info.first().song_id).save()
                            return JsonResponse({'status': 'success', 'message': _('Read plot successfully')})
                    elif chapter.exists():
                        if ChapterUnlock.objects.filter(user_id=user_id, chapter_id=chapter.first().chapter_id):
                            return JsonResponse({'status': 'error',
                                                 'message': _('You have already unlocked this chapter')}, status=400)
                        else:
                            ChapterUnlock.objects.create(user_id=user_id,
                                                         chapter_id=chapter.first().chapter_id).save()
                            return JsonResponse({'status': 'success', 'message': _('Read plot successfully')})
                    else:
                        return JsonResponse({'status': 'error',
                                             'message': _('This Plot does not belong to any song or chapter')},
                                            status=400)
                else:
                    return JsonResponse({'status': 'error',
                                         'message': _('Please read the previous plot first')}, status=400)
            else:
                return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)
