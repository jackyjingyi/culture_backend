from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, UserManager, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.core.mail import send_mail
from nanoid import generate


def nanoid_generate():
    return generate(size=24)


class User(AbstractBaseUser, PermissionsMixin):
    # 管理账户类
    id = models.CharField(_('用户ID'), max_length=25, default=nanoid_generate, primary_key=True)
    username_validator = UnicodeUsernameValidator()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    username = models.CharField(
        _("用户名"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    name = models.CharField(_("姓名"), max_length=150, blank=True)
    email = models.EmailField(_("邮箱"), blank=True)
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    is_staff = models.BooleanField(
        _("员工"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("激活"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    company = models.CharField(_('公司ID'), max_length=25, null=True, blank=True)
    date_joined = models.DateTimeField(_("加入时间"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_short_name(self):
        """Return the short name for the user."""
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
