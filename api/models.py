from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser
from django.db.models import CharField, UUIDField


class User(AbstractBaseUser):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    username = CharField(max_length=150, unique=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
