from django import forms
from .models import Domain


class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ['name', 'expiration_date', 'registrar']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'example.com',
                'required': True
            }),
            'expiration_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'registrar': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Reg.ru, GoDaddy и т.д.'
            })
        }

    def clean_name(self):
        name = self.cleaned_data['name'].lower().strip()
        # Убираем http://, https:// и www.
        if name.startswith('http://'):
            name = name[7:]
        elif name.startswith('https://'):
            name = name[8:]
        if name.startswith('www.'):
            name = name[4:]
        return name