import uuid

from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _

from desert import settings


class RequestRestrictionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        identify = request.session.get('identify')
        requested_times = cache.get(identify)
        if requested_times is not None:
            if int(requested_times) >= settings.REQUEST_LIMIT:
                return JsonResponse({'status': 'error', 'message': _('Too many requests')}, status=400)
            else:
                cache.set(identify, requested_times + 1)
        else:
            identify = request.session['identify'] = uuid.uuid4()
            cache.set(identify, 1, settings.REQUEST_LIMIT_TIME)
