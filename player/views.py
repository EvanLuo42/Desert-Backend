from django.contrib.auth import get_user_model, authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from player.forms import LoginForm, RegisterForm, AddFriendForm
from player.models import Friend

User = get_user_model()


def users_dump(users):
    return [{
        'user_id': user.user_id,
        'user_name': user.user_name,
        'ptt': user.ptt,
        'last_login': str(user.last_login),
    } for user in users]


def user_dump(user):
    return {
        'user_id': user.user_id,
        'user_name': user.user_name,
        'ptt': user.ptt,
        'last_login': str(user.last_login),
    }


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            user = authenticate(username=user_name, password=password)

            if user:
                login(request, user)
                user = User.objects.get(user_name=user_name)
                request.session['user_id'] = user.user_id

                return JsonResponse({'status': 'success', 'message': 'Login Successful'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid Credentials'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid Form'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid Request'})


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            user = User.objects.create_user(user_name, password)
            user.save()

            return JsonResponse({'status': 'success', 'message': 'Registration Successful'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid Form'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid Request'})


@csrf_exempt
def add_friend_view(request):
    if request.method == 'GET':
        form = AddFriendForm(request.GET)
        if form.is_valid() and request.user.is_authenticated:
            friend_id = form.clean_friend_id()
            user_id = request.session.get('user_id')
            if friend_id == user_id:
                return JsonResponse({'status': 'error', 'message': 'You can not add yourself as friend'})
            elif [friend.user_id == user_id for friend in Friend.objects.filter(friend_id=friend_id)]:
                return JsonResponse({'status': 'error', 'message': 'You have added the friend already'})
            else:
                friend = Friend.objects.create(user_id=user_id, friend_id=friend_id)
                friend.save()

                return JsonResponse({'status': 'success', 'message': 'Friend Added'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid Form'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid Request'})


@csrf_exempt
def get_friends_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_id = request.session.get('user_id')
            friends = Friend.objects.filter(user_id=user_id)
            friends_list = [User.objects.get(user_id=friend.friend_id) for friend in friends]

            return JsonResponse({'status': 'success', 'friends': users_dump(friends_list)})
        else:
            return JsonResponse({'status': 'error', 'message': 'You have not logged in yet'})
    else:
        return JsonResponse({'status': 'error', 'friends': 'Invalid Request'})


@csrf_exempt
def delete_friend_view(request):
    if request.method == 'GET':
        form = AddFriendForm(request.GET)
        if form.is_valid() and request.user.is_authenticated or request.user.is_superuser:
            user_id = request.session.get('user_id')
            friend_id = form.clean_friend_id()
            if Friend.objects.filter(friend_id=friend_id, user_id=user_id).exists():
                Friend.objects.filter(friend_id=friend_id, user_id=user_id).delete()
                return JsonResponse({'status': 'success', 'message': 'Friend Deleted'})
            else:
                return JsonResponse({'status': 'error', 'message': 'You have not added the friend yet'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid Form'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid Request'})
