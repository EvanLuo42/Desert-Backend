from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class PlayerManager(BaseUserManager):
    def _create_user(self, user_name, password, **kwargs):
        if not user_name:
            raise ValueError('The given username must be set')
        if not password:
            raise ValueError('The given password must be set')
        user = self.model(user_name=user_name, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_name, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(user_name, password, **kwargs)

    def create_superuser(self, user_name, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(user_name, password, **kwargs)


class Player(AbstractBaseUser, PermissionsMixin):
    user_id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    rank_point = models.FloatField(default=0)
    grade = models.IntegerField(default=1)

    selected_role = models.CharField(max_length=30, default='')

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['is_staff', 'is_superuser']

    objects = PlayerManager()


class Friend(models.Model):
    id = models.BigAutoField(primary_key=True)
    friend_id = models.IntegerField()
    user_id = models.IntegerField()
