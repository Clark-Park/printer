from django.forms import ModelForm
from .models import Company, Copier


class CopierForm(ModelForm):
    class Meta:
        model = Copier
        fields = ('company', 'color_mono', 'bit', 'model_name', 'driver_file')
