from django.db import models


class Service(models.Model):
    """
    The model describes a registered service
    """
    class Meta:
        db_table = 'service'

    #  A registered service name
    service_name = models.CharField(max_length=512,
                                    null=False,
                                    blank=False,
                                    help_text='A registered service name')
    # The service's unique key; can be used to share access rights with other services
    service_key = models.CharField(max_length=128,
                                   null=False,
                                   blank=False)


class AccessServiceRights(models.Model):
    """
    The model describes rights set, which a registered service can provide to
    """
    class Meta:
        db_table = 'service_rights'

    # The access rights source service
    provider = models.ForeignKey('service_registrar.Service',
                                 null=False,
                                 blank=False,
                                 related_name='asr_provider',
                                 help_text='The access rights source service')
    # Services sharing access rights;
    services = models.ManyToManyField('service_registrar.Service',
                                      related_name='asr_set')
