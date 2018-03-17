from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .models import KirrURL
from .forms import SumbitUrlForm
from .validators import validate_url
# Create your views here.

def about(request):
    return HttpResponse("About Me!!")

#function based view
def RedirectURL(request, shortcode=None, *args, **kwargs):

    obj = get_object_or_404(KirrURL, shortcode=shortcode)
    clicks = obj.clicks
    KirrURL.objects.filter(shortcode=shortcode).update(clicks=clicks+1)
    print("Redirecting to: {}".format(obj.url))
    return HttpResponseRedirect(obj.url)
    """
    obj = KirrURL.objects.filter(shortcode = shortcode)
    if obj.exists() and obj.count()==1:
        return HttpResponse("Hello from {}".format(obj.first().url))
    return HttpResponse("Invalide URL!!")
    """

class HomeView(View):
    def get(self, request, *args, **kwargs):
        form = SumbitUrlForm()
        context = {
            'title': "Mini.com",
            'form' : form
        }
        print("GET",context)
        return render(request, "shortner/home.html", context)

    def post(self, request, *args, **kwargs):
        form = SumbitUrlForm(request.POST)
        template = "shortner/home.html"
        context = {
            'title': "Mini.com",
            'form' : form
        }
        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            new_url = validate_url(new_url)
            obj, created = KirrURL.objects.get_or_create(url=new_url)
            context = {
                'object':obj,
                'created':created
            }
            if created:
                template = "shortner/success.html"
            else:
                template = "shortner/exists.html"
        return render(request, template, context)

"""
class CBview(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        return HttpResponse("Hello from Class by {}".format(shortcode))
"""