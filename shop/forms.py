from django.forms import ModelForm
from .models import Items

class addItem(ModelForm):
    class Meta:
        model=Items
        fields=('name','description','price','image',)