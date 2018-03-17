from django import forms
from .validators import validate_url

class SumbitUrlForm(forms.Form):
    url = forms.CharField(label='Submit Form', validators=[validate_url])
