from django.contrib.auth import get_user_model
from django.forms import Form, fields
from django.utils.translation import gettext as _

User = get_user_model()


class LoginForm(Form):
    user_name = fields.CharField(
        required=True,
        min_length=4,
        max_length=30,
        error_messages={
            'required': _('Username can not be empty.'),
            'min_length': _('Username is too short.'),
            'max_length': _('Username is too long.')
        }
    )

    password = fields.CharField(
        required=True,
        error_messages={
            'required': _('Password can not be empty.')
        }
    )


class RegisterForm(Form):
    user_name = fields.CharField(
        required=True,
        min_length=4,
        max_length=30,
        error_messages={
            'required': _('Username can not be empty.'),
            'min_length': _('Username is too short.'),
            'max_length': _('Username is too long.')
        }
    )

    password = fields.CharField(
        required=True,
        error_messages={
            'required': _('Password can not be empty.')
        }
    )

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if User.objects.filter(user_name=user_name).exists():
            raise fields.ValidationError(_('User is already exist.'))
        else:
            return user_name


class AddFriendForm(Form):
    friend_id = fields.IntegerField(
        required=True,
        error_messages={
            'required': _('Friend ID can not be empty.')
        }
    )

    def clean_friend_id(self):
        friend_id = self.cleaned_data.get('friend_id')
        if User.objects.filter(user_id=friend_id).exists():
            return friend_id
        else:
            raise fields.ValidationError(_('User does not exist.'))


class GetPlayerForm(Form):
    user_id = fields.IntegerField(
        required=True,
        error_messages={
            'required': _('User ID can not be empty.')
        }
    )

    def clean_user_id(self):
        user_id = self.cleaned_data.get('user_id')
        if User.objects.filter(user_id=user_id).exists():
            return self.cleaned_data.get('user_id')
        else:
            raise fields.ValidationError(_('User does not exist.'))
