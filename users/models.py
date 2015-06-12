from django.db import models
from django.utils.timezone import now
from django.core.urlresolvers import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


from users.utils import send_template_mail, default_token_generator


class UserManager(BaseUserManager):
    def _create_user(self, email, password,
                    is_staff, is_superuser, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email, last_login=now(), date_joined=now(),
            is_active=True, is_staff=is_staff, is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True, blank=False)
    full_name = models.CharField(_('name'), max_length=30, blank=False)

    is_verified = models.BooleanField(_('verified'), default=False)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.full_name.partition(' ')[0]

    def get_full_name(self):
        return self.full_name

    def send_verification_mail(self, request):
        if not self.pk:
            self.save()

        return send_template_mail(
            'Verificação de email',
            'users/user_verification_email.html',
            {
                'user': self,
                'verification_url': request.build_absolute_uri(
                    reverse('users:user_verify', kwargs={
                        'uidb64': urlsafe_base64_encode(force_bytes(self.pk)),
                        'token': default_token_generator.make_token(self)
                    })
                )
            },
            [self.email]
        )
