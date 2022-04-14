from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


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
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(user_name, password, email, birth, **kwargs)


class Player(AbstractBaseUser, PermissionsMixin):
    user_id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    rank_point = models.FloatField(default=0)
    grade = models.IntegerField(default=1)
    email = models.EmailField(unique=True)
    birth = models.DateField()

    selected_role = models.IntegerField(default=1)

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['is_staff', 'is_superuser', 'email', 'birth']

    objects = PlayerManager()


class Friend(models.Model):
    id = models.BigAutoField(primary_key=True)
    friend_id = models.IntegerField()
    user_id = models.IntegerField()
