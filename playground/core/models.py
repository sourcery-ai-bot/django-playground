from django.db import models
from django.utils.translation import gettext_lazy as _

from playground.core.validators import *


class BaseModel(models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('created at'), auto_now=True)

    class Meta:
        abstract = True


class Person(BaseModel):
    name = models.CharField(_('name'), max_length=128)
    nickname = models.CharField(_('nickname'), max_length=32)
    document = models.CharField(_('document'), max_length=14, validators=[validate_document])
    phone = models.CharField(_('phone'), max_length=11, validators=[validate_phone])


class NaturalPerson(Person):
    GENDER = [('M', _('Male')), ('F', _('Female')), ('O', _('Other'))]

    person = models.OneToOneField(
        to=Person,
        on_delete=models.CASCADE,
        parent_link=True,
        verbose_name=_('person')
    )
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER)
    birthday = models.DateField(_('birthday'))


class LegalPerson(Person):
    person = models.OneToOneField(
        to=Person,
        on_delete=models.CASCADE,
        parent_link=True,
        verbose_name=_('person')
    )
    state_registration = models.CharField(_('state registration'), max_length=32)
    municipal_registration = models.CharField(_('municipal registration'), max_length=32)
