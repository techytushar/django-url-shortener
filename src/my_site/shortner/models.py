from django.db import models
from .utils import create_shortcode
#import variables from settings
from django.conf import settings
from .validators import validate_url

#making a model manager to override the default (used in shell)
class KirrURLManager(models.Manager):
    def all(self, *args, **kwargs):
        qs = super(KirrURLManager, self).all(*args, **kwargs).filter(active=True)
        return qs
    #to refresh all shortcodes using model manager
    def refresh_shortcodes(self):
        qs = KirrURL.objects.filter(id__gte=1)
        count = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            q.save()
            count += 1
        return "Shortcodes changed: {}".format(count)

#if value not present in settings set it to 20
SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 20)

class KirrURL(models.Model):
    url = models.CharField(max_length=200, validators=[validate_url])
    shortcode = models.CharField(max_length=SHORTCODE_MAX, null=False, blank=False, unique=True)
    updated  = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    clicks = models.IntegerField(default=0)

    #linking the model manager
    #object = KirrURLManager

    #overriding the save method
    def save(self, *args, **kwargs):
        if self.shortcode==None or self.shortcode=="":
            self.shortcode = create_shortcode(self)
        super(KirrURL, self).save(*args, **kwargs)

    #string format displayed in the admin panel
    """
    def __str__(self):
        return ("{} - {} - {}".format(self.url, self.shortcode, self.updated))
    
    def __unicode__(self):
        return str(self.url)
    """
    def get_short_url(self):
        short_url = settings.DEFAULT_REDIRECT_URL + '/' + self.shortcode
        return short_url