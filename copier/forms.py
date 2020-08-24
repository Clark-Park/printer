from django import forms
from .models import Company, Copier


class CopierForm(forms.ModelForm):
    class Meta:
        model = Copier
        fields = ('company', 'color_mono', 'bit', 'model_name', 'driver_file')


class CompanyScannerForm(forms.ModelForm):

    scanner = forms.FileField(required=True)

    def __init__(self, *args, **kwargs):
        super(CompanyScannerForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True

    class Meta:
        model = Company
        fields = ('name', 'scanner')
