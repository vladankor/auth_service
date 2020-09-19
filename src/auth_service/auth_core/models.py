from django.db import models

from py_kor.types import ChoiceEnum


class User(models.Model):
    """
    Модель, описывающая пользователя
    """
    class Meta:
        db_table = 'user'
        constraints = [
            models.CheckConstraint(check=(models.Q(phone_number__isnull=False) | models.Q(email__isnull=False)),
                                   name='identifier_is_not_null'),
        ]

    phone_number = models.CharField(max_length=64,
                                    null=True,
                                    blank=True)
    email = models.EmailField(max_length=256,
                              null=True,
                              blank=True)
    password = models.CharField(max_length=128,
                                null=False,
                                blank=False)


class Rights(ChoiceEnum):
    """
    Внутренние права
    """
    GUEST = 0
    ADMINISTRATOR = 1


class Group(models.Model):
    """
    Модель, описывающая группу пользователей по разделению прав
    """
    class Meta:
        db_table = 'group'

    users = models.ManyToManyField(to=User,
                                   blank=True,
                                   related_name='groups',
                                   default=list())
    right = models.IntegerField(default=Rights.GUEST.value,
                                choices=Rights.choices())
