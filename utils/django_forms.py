import re
from django.core.exceptions import ValidationError

def add_attrs(field, attr_name, attr_value):
    if field:
        field.widget.attrs[attr_name] = attr_value

def add_placeholder(field, placeholder_val):
     field.widget.attrs['placeholder'] = placeholder_val

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@,#,$,%,¨,&,*,!,/,-,+,.]).{8,}$')
    if not regex.match(password):
        raise ValidationError(
            ('Passoword invalid!'),
            code='invalid'
        )