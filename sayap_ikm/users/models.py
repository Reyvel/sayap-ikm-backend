from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ImageField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    OWNER = 'OW'
    INVESTOR = 'IV'
    ROLE_CHOICES = (
        (OWNER, 'owner'),
        (INVESTOR, 'investor'),
    )

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    image = ImageField(null=True)
    role = CharField(max_length=10, choices=ROLE_CHOICES, default=INVESTOR)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
