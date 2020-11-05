from django.db import models

from utilities.model_mixins.created import MixCreated
from utilities.model_mixins.modified import MixModified

from py_kor.pk_mixins import ChoiceEnum


class ServiceType(ChoiceEnum):
    WEB_APPLICATION = 'web application'
    USER_AGENT_BASED_APPLICATION = 'user agent based application'
    NATIVE_APPLICATION = 'native application'


class Service(MixCreated, MixModified):
    """
    Model represents registered service
    """
    class Meta:
        db_table = 'service'

    # Unique service ID
    uuid = models.UUIDField(primary_key=True,
                            null=False,
                            blank=False)

    # Service name (other) https://tools.ietf.org/html/rfc6749#section-2.1
    name = models.CharField(max_length=128,
                            null=False,
                            blank=False)

    # Service type (required) https://tools.ietf.org/html/rfc6749#section-2.1
    type = models.CharField(max_length=32,
                            null=False,
                            blank=False,
                            choices=ServiceType.choices())

    # Client redirection URI (required) https://tools.ietf.org/html/rfc6749#section-3.1.2
    client_redirection_uri = models.CharField(max_length=512,
                                              null=False,
                                              blank=False)

    # Secret
    secret = models.CharField(max_length=36,
                              null=False,
                              blank=False)

    service_password = models.CharField(max_length=128,
                                        null=False,
                                        blank=False)


class ServiceSession(models.Model):
    class Meta:
        db_table = 'service_token'

    service = models.ForeignKey(to='service.Service',
                                null=False,
                                blank=False,
                                on_delete=models.CASCADE,
                                related_name='service_tokens')

    # Session access token
    authentication_token = models.CharField(max_length=512,
                                            null=False,
                                            blank=False)

    # Authentication token expire time
    expires_at = models.DateTimeField(null=False,
                                      blank=False)

    # Session refresh token
    refresh_token = models.CharField(max_length=512,
                                     null=True,
                                     blank=True)
