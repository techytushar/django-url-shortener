import random
import string
from django.conf import settings

SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 6)

# generate a new shortcode
def shortcode_generator():
    chars = string.ascii_letters+string.digits
    size = SHORTCODE_MIN
    return ''.join(random.choice(chars) for _ in range(size))

#importing the class from models and checking if the url exists
def create_shortcode(instance, size=6):
    code = shortcode_generator()
    kirr_class = instance.__class__
    exists = kirr_class.objects.filter(shortcode=code).exists()
    if exists:
        return create_shortcode(size=size)
    return code 