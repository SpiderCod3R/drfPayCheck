from django.db import models
from django.contrib.auth import get_user_model

from django.contrib.auth.models import AbstractUser, BaseUserManager
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _


class Base(models.Model):
    created_at = models.DateTimeField(_('Criado em'), auto_now=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)
    is_active = models.BooleanField(_('Esta Ativo?'), default=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('User must have an username')

        _user_ = self.model(username=username, **extra_fields)
        _user_.set_password(password)
        _user_.save(using=self.db)

        # Criando Token apos criar o usuário
        Token.objects.create(user=_user_)
        return _user_

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super User must have is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super User must have is_staff=True')

        return self._create_(username, password, **extra_fields)


class CustomUser(AbstractUser, Base):
    username = models.CharField(_('Login'), max_length=50, unique=True)
    is_staff = models.BooleanField(_('Membro da Equipe?'), default=True)

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username

    def __token__(self):
        return Token.objects.get(user=self)

    objects = UserManager()


class Function(Base):
    name = models.CharField('Nome', max_length=50)

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return self.name


class BusinessLocation(Base):
    name = models.CharField('Nome', max_length=50)

    class Meta:
        verbose_name = 'Local de Trabalho'
        verbose_name_plural = 'Locais de Trabalho'

    def __str__(self):
        return self.name


class Profile(Base):
    user = models.ForeignKey(CustomUser, verbose_name="Usuário", on_delete=models.CASCADE)
    name = models.CharField('Nome', max_length=50)
    business = models.ForeignKey(BusinessLocation, verbose_name='Contrato', on_delete=models.PROTECT)
    function = models.ForeignKey(Function, verbose_name='Cargo', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return f'{self.name} - {self.business}'


