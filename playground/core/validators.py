import re

from django.core.validators import RegexValidator


def validate_document(document):
    validator = RegexValidator(
        regex=re.compile(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'),
        message='The document must be in the format xxx.xxx.xxx-xx, where "x" is a digit.'
    )
    validator(document)


def validate_phone(phone):
    validator = RegexValidator(
        regex=re.compile('^d{11}$'),
        message='The phone must contain 11 digits only.'
    )
    validator(phone)
