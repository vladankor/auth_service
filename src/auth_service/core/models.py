from django.db import models

from utilities.model_mixins.created import MixCreated
from utilities.model_mixins.modified import MixModified


class User(MixCreated, MixModified):
    """
    Model represents user
    """
    class Meta:
        db_table = 'user'
        constraints = [
            models.CheckConstraint(check=(models.Q(phone_number__isnull=False) | models.Q(email__isnull=False)),
                                   name='identifier_is_not_null'),
        ]

    # User phone number
    phone_number = models.CharField(max_length=64,
                                    null=True,
                                    blank=True)

    # User email
    email = models.EmailField(max_length=256,
                              null=True,
                              blank=True)

    # Hashed user password
    password = models.CharField(max_length=256,
                                null=False,
                                blank=False)

    # Is user profile verified by any source. Verify sources:
    # - email
    is_verified = models.BooleanField(default=False,
                                      null=False,
                                      blank=False)

    # Unique user ID
    uuid = models.CharField(max_length=144,
                            null=False,
                            blank=False)


class Session(MixCreated, MixModified):
    """
    Model represents user session with optional registered device
    """
    class Meta:
        db_table = 'session'

    # Session access token
    authentication_token = models.CharField(max_length=2048,
                                            null=False,
                                            blank=False)

    # Session refresh token
    refresh_token = models.CharField(max_length=256,
                                     null=False,
                                     blank=False)

    # Service session key created for
    service = models.ForeignKey(to='service.Service',
                                null=False,
                                blank=False,
                                on_delete=models.CASCADE,
                                related_name='sessions')

    user = models.ForeignKey(to='core.User',
                             null=False,
                             blank=False,
                             on_delete=models.CASCADE,
                             related_name='sessions')

    # Session expire time
    expires_at = models.DateTimeField(null=False,
                                      blank=False)
