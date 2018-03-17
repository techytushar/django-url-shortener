from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def validate_url(value):
    url_validator = URLValidator()
    value1_invalid = False
    value2_invalid = False
    new_value = ""
    try:
        url_validator(value)
    except:
        value1_invalid = True
    
    if value1_invalid:
        new_value = "http://"+value
        try:
            url_validator(new_value)
        except:
            value2_invalid = True
    
    if value1_invalid and value2_invalid:
        raise ValidationError("Enter a valid URL")

    if new_value=="":
        new_value = value
    return new_value