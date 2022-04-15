from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _
from django_otp.models import Device, DeviceManager
from django_otp.plugins.otp_totp.models import TOTPDevice


class PlayerManager(BaseUserManager):
    def _create_user(self, user_name, password, email, birth, **kwargs):
        if not user_name:
            raise ValueError('The given username must be set')
        if not password:
            raise ValueError('The given password must be set')
        if not email:
            raise ValueError('The given email must be set')
        if not birth:
            raise ValueError('The given birth must be set')

        user = self.model(user_name=user_name, email=email, birth=birth, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    @staticmethod
    def create_user(self, user_name, password, email, birth, **kwargs):
        kwargs['is_superuser'] = False
        kwargs['is_staff'] = False
        return self._create_user(user_name, password, email, birth, **kwargs)

    def create_superuser(self, user_name, password, email, birth, **kwargs):
        return self._create_user(user_name, password, email, birth, **kwargs)


class Player(AbstractBaseUser, PermissionsMixin):
    user_id = models.BigAutoField(primary_key=True, verbose_name=_('User ID'))
    user_name = models.CharField(max_length=30, unique=True, verbose_name=_('Username'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Is a stuff'))
    is_superuser = models.BooleanField(default=False, verbose_name=_('Is a superuser'), )
    rank_point = models.FloatField(default=0, verbose_name=_('Rank point'))
    grade = models.IntegerField(default=1, verbose_name=_('Grade'))
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    birth = models.DateField(verbose_name=_('Birth'))

    selected_role = models.IntegerField(default=1)

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['is_staff', 'is_superuser', 'email', 'birth']

    objects = PlayerManager()

    class Meta:
        verbose_name = _('Player')
        verbose_name_plural = verbose_name


class Friend(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name=_('ID'))
    friend_id = models.IntegerField(verbose_name=_('Friend ID'))
    user_id = models.IntegerField(verbose_name=_('User ID'))

    class Meta:
        verbose_name = _('Friend')
        verbose_name_plural = verbose_name
