from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _

from desert import settings, constant


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
        if [request.path.find(path) != -1 for path in constant.SAFEGUARD_IGNORE]:
            pass
        else:
            if settings.SAFEGUARD_MODE:
                return JsonResponse({'status': 'error', 'message': _('Server is under maintenance')}, status=503)


class UserAgentMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_agent = request.headers.get('User-Agent').split(' ')
        path_time = 0
        for path in constant.USER_AGENT_IGNORE:
            if request.path.find(path) != -1:
                path_time = path_time + 1
                break

        if path_time == 0:
            if len(user_agent) != 2 or len(user_agent[1].split('/')) != 2:
                return JsonResponse({'status': 'error', 'message': _('Argument missing')}, status=400)
            elif user_agent[0] != constant.PROJECT_NAME + '/' + settings.API_VERSION:
                return JsonResponse({'status': 'error', 'message': _('API version does not support')}, status=400)
            elif user_agent[1].split('/')[0] not in constant.SUPPORT_DEVICE:
                return JsonResponse({'status': 'error', 'message': _('Platform does not support')}, status=400)
