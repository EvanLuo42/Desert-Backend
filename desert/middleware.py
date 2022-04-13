from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _

from desert import settings


class RateLimitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        identify = request.META.get('REMOTE_ADDR')
        requested_times = cache.get(identify)
        if requested_times is not None:
            if int(requested_times) >= settings.REQUEST_LIMIT:
                return JsonResponse({'status': 'error', 'message': _('Too many requests')}, status=400)
            else:
                cache.set(identify, requested_times + 1)
        else:
            cache.set(identify, 1, settings.REQUEST_LIMIT_TIME)


class ServerSafeGuardMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if settings.SAFEGUARD_MODE:
            return JsonResponse({'status': 'error', 'message': _('Server is under maintenance')}, status=503)


class UserAgentMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_agent = request.headers.get('User-Agent').split(' ')
        if request.path.find('/desert/admin/') != -1 or request.path.find('/static/') != -1:
            pass
        elif len(user_agent) != 2 or len(user_agent[1].split('/')) != 2:
            return JsonResponse({'status': 'error', 'message': _('Argument missing')}, status=400)
        elif user_agent[0] != 'Desert/' + settings.API_VERSION:
            return JsonResponse({'status': 'error', 'message': _('API version does not support')}, status=400)
        elif user_agent[1].split('/')[0] != 'Android' and user_agent[1].split('/')[0] != 'iOS' \
                and user_agent[1].split('/')[0] != 'iPadOS':
            return JsonResponse({'status': 'error', 'message': _('Platform does not support')}, status=400)
