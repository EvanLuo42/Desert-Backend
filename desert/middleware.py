import datetime

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _


class RequestRestrictionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        last_request = request.session.get('last_request')
        now = datetime.datetime.now()
        if last_request is not None:
            last_request = datetime.datetime.strptime(request.session.get('last_request'), '%Y-%m-%d %H:%M:%S.%f')
            if (now - last_request).seconds < 2:
                return JsonResponse({'status': 'error', 'message': _('To many request')}, status=400)
            else:
                request.session['last_request'] = str(now)
        else:
            request.session['last_request'] = str(now)



