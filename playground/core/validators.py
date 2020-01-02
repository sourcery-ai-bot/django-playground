import re

from django.core.validators import RegexValidator


def validate_document(document):
    validator = RegexValidator(regex=re.compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"))
    validator(document)


def validate_phone(phone):
    validator = RegexValidator(regex=re.compile("^d{11}$"))
    validator(phone)
