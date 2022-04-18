import uuid

from django.core.cache import cache
from django.http import JsonResponse
from django.utils.translation import gettext as _

from desert import constant
from link.form import ValidTokenForm


def get_link_token_view(request):
    if request.method == constant.GET_METHOD:
        if request.user.is_authenticated:
            cache.set(request.session.get('user_id'), str(uuid.uuid4()), 60 * 60 * 12)
            return JsonResponse({'status': 'success', 'token': cache.get(request.session.get('user_id'))})
        else:
            return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def is_token_available_view(request):
    if request.method == constant.GET_METHOD:
        form = ValidTokenForm(request.GET)
        if form.is_valid():
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)
