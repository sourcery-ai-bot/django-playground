from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from playground.core.validators import *


class BaseModel(models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        abstract = True


class BaseUserModel(BaseModel):
    created_by: models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        related_name='created_%(class)s'
    )
    modified_by: models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        related_name='modified_%(class)s'
    )

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


class Shop(BaseUserModel):
    owner = models.ForeignKey(
        to=Person,
        on_delete=models.CASCADE,
        related_name='shops',
        related_query_name='shop',
        verbose_name=_('owner')
    )
    name = models.CharField(_('name'), max_length=128)
    default_currency = models.CharField(_('default currency'), max_length=3)
    value_increase = models.DecimalField(
        _('value increase'),
        decimal_places=4,
        max_digits=5,
        validators=[MinValueValidator(0)]
    )


class Product(models.Model):
    shop = models.ForeignKey(
        to=Shop,
        on_delete=models.CASCADE,
        related_name='products',
        related_query_name='product',
        verbose_name=_('shop')
    )
    name = models.CharField(_('name'), max_length=128)
    price = models.DecimalField(_('price'), decimal_places=2, max_digits=11, validators=[MinValueValidator(0)])
    currency = models.CharField(_('currency'), max_length=3)
    quantity = models.PositiveSmallIntegerField(_('quantity'))


class ShoppingList(BaseUserModel):
    shop = models.ForeignKey(
        to=Shop,
        on_delete=models.CASCADE,
        related_name='shopping_lists',
        related_query_name='shopping_list',
        verbose_name=_('shop')
    )
    products = models.ManyToManyField(
        to=Product,
        related_name='products',
        related_query_name='product',
        verbose_name=_('product')
    )
    currency_used = models.CharField(_('currency used'), max_length=3)
    dollar_value = models.DecimalField(
        _('dollar value'),
        decimal_places=2,
        max_digits=4,
        validators=[MinValueValidator(0)]
    )
