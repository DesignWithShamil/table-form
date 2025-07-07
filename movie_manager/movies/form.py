from django.forms import ModelForm
from . models import movieinfo

class movieForm(ModelForm):
    class Meta:
        model=movieinfo
        fields='__all__'