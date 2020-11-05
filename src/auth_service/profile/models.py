from django.db import models

from core.models import User
from py_kor.pk_mixins import ChoiceEnum


class Gender(ChoiceEnum):
    UNKNOWN = 0
    MAN = 1
    WOMAN = 2
    OTHER = 3


class UserProfile(models.Model):
    user = models.OneToOneField(to=User,
                                related_name='user_profile',
                                on_delete=models.CASCADE,
                                primary_key=True)

    name = models.CharField(max_length=128,
                            blank=True,
                            default='')

    patronymic = models.CharField(max_length=128,
                                  blank=True,
                                  default='')

    surname = models.CharField(max_length=128,
                               blank=True,
                               default='')

    birth_date = models.DateTimeField(blank=True,
                                      auto_now_add=True)

    gender = models.IntegerField(default=Gender.UNKNOWN.value,
                                 choices=Gender.choices())