import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from userprofile.utils import NoServerAvailableException, NoUserEmailException

from projects import models as project_models


class Server(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField(max_length=200)
    max_users = models.IntegerField(default=0)

    @property
    def users(self):
        return User.objects.filter(server=self)

    def __str__(self):
        return f'{str(self.id)}-{str(self.url)}'


class UserManager(BaseUserManager):
    """Custom user model manager with email field as the unique identifier"""

    def create_user(self, email, username, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """Creating a superuser with ADMIN role"""
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(email, username, password, **extra_fields)
        return user


class User(AbstractUser):

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"
        ordering = ['username']
        unique_together = ['username', 'email', 'project']

    token = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    email = models.EmailField(
        unique=False,
        max_length=255
    )
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    # user should be able to have multiple projects
    project = models.OneToOneField(
        project_models.Project,
        on_delete=models.CASCADE,
        related_name='user',
        null=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    # Username and Email should be required for login
    REQUIRED_FIELDS = ['email']

    @property
    def active_server(self):
        if self.server:
            return self.server.url

    def expire_token(self):
        """Blacklist last refresh_token"""
        try:
            last = OutstandingToken.objects.filter(
                user=self).latest('created_at')
            token = RefreshToken(last.token)
            token.blacklist()
        except ObjectDoesNotExist:
            pass
        except TokenError:
            """If this token is present in the token blacklist. TokenError will be raise."""
            pass

    def refresh_token(self):
        """Blacklist last token and generate a new pair"""
        self.expire_token()
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}

    def save(self, *args, **kwargs):
        """Overriding save method to set server url base on server max_users"""
        if not self.server:
            for server in Server.objects.all():
                if server.max_users > server.users.count():
                    self.server = server
                    break
        # raise error if no server is available
        if not self.server and not self.is_superuser:
            raise NoServerAvailableException('No server available')

        # raise error if user email not provided
        if not self.email:
            raise NoUserEmailException('Email is required')
        super(User, self).save(*args, **kwargs)
