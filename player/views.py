# -*- coding: utf-8 -*-
import random
import string

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _

from player.forms import LoginForm, RegisterForm, AddFriendForm, GetPlayerForm, EmailForm, ResetPasswordForm
from player.models import Friend

User = get_user_model()


def users_dump(users):
    return [{
        'user_id': user.user_id,
        'user_name': user.user_name,
        'rank_point': user.rank_point,
        'grade': user.grade,
        'selected_role': user.selected_role,
        'last_login': str(user.last_login),
    } for user in users]


def user_dump(user):
    return {
        'user_id': user.user_id,
        'user_name': user.user_name,
        'rank_point': user.rank_point,
        'grade': user.grade,
        'selected_role': user.selected_role,
        'last_login': str(user.last_login),
    }


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('user_name')
            password = form.cleaned_data.get('password')
            user = authenticate(username=user_name, password=password)

            if user:
                user = User.objects.get(user_name=user_name)
                if not user.is_superuser:
                    login(request, user)
                    request.session['user_id'] = user.user_id
                    return JsonResponse({'status': 'success', 'message': _('Login Successful')})
                else:
                    return JsonResponse({'status': 'success', 'message': _('You can not login as a superuser')},
                                        status=401)
            else:
                return JsonResponse({'status': 'error', 'message': _('Invalid Credentials')}, status=401)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('user_name')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            birth = form.cleaned_data.get('birth')
            user = User.objects.create_user(user_name, password, email)
            user.save()

            return JsonResponse({'status': 'success', 'message': _('Registration Successful')})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


async def send_captcha_view(request):
    if request.method == 'GET':
        form = EmailForm(request.GET)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            captcha = ''.join(random.sample(string.ascii_letters + string.digits, 5))
            cache.set(email, captcha, 600 * 5)
            send_mail(
                _('Desert Captcha'),
                captcha,
                'luo_evan@163.com',
                [email],
                fail_silently=False,
            )
            return JsonResponse({'status': 'success', 'message': _('Captcha Sent')})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


@csrf_exempt
def reset_password_view(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(email=email).first()
            user.set_password(password)
            user.save()
            return JsonResponse({'status': 'success', 'message': _('Password Reset')})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def logout_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'status': 'success', 'message': _('Logout Successful')})
        else:
            return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def add_friend_view(request):
    if request.method == 'GET':
        form = AddFriendForm(request.GET)
        if form.is_valid():
            if request.user.is_authenticated:
                friend_id = form.clean_friend_id()
                user_id = request.session.get('user_id')
                if friend_id == user_id:
                    return JsonResponse({'status': 'error', 'message': _('You can not add yourself as friend')},
                                        status=400)
                elif [friend.user_id == user_id for friend in Friend.objects.filter(friend_id=friend_id)]:
                    return JsonResponse({'status': 'error', 'message': _('You have added the friend already')}, status=400)
                else:
                    friend = Friend.objects.create(user_id=user_id, friend_id=friend_id)
                    friend.save()

                    return JsonResponse({'status': 'success', 'message': _('Friend Added')})
            else:
                return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def get_friends_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_id = request.session.get('user_id')
            friends = Friend.objects.filter(user_id=user_id)
            friends_list = [User.objects.get(user_id=friend.friend_id) for friend in friends]

            return JsonResponse({'status': 'success', 'friends': users_dump(friends_list)})
        else:
            return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
    else:
        return JsonResponse({'status': 'error', 'friends': _('Invalid Request')}, status=405)


def delete_friend_view(request):
    if request.method == 'GET':
        form = AddFriendForm(request.GET)
        if form.is_valid():
            if request.user.is_authenticated:
                user_id = request.session.get('user_id')
                friend_id = form.clean_friend_id()
                if Friend.objects.filter(friend_id=friend_id, user_id=user_id).exists():
                    Friend.objects.filter(friend_id=friend_id, user_id=user_id).delete()
                    return JsonResponse({'status': 'success', 'message': _('Friend Deleted')})
                else:
                    return JsonResponse({'status': 'error', 'message': _('You have not added the friend yet')}, status=404)
            else:
                return JsonResponse({'status': 'error', 'message': _('You have to login first')}, status=401)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def get_all_players_view(request):
    if request.method == 'GET':
        return JsonResponse({'status': 'success', 'players': users_dump(User.objects.all())})
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def get_player_view(request):
    if request.method == 'GET':
        form = GetPlayerForm(request.GET)
        if form.is_valid():
            user_id = form.clean_user_id()
            user = User.objects.get(user_id=user_id)
            return JsonResponse({'status': 'success', 'player': user_dump(user)})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid Request')}, status=405)


def page_not_found(request, exception):
    return JsonResponse({'status': 'error', 'message': _('Page Not Found')}, status=404)
