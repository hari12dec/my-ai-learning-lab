from django import forms
from .models import *


class fakenewsForm(forms.ModelForm):
    class Meta():
        model=fakenewsModel
        fields=['fakenews']
