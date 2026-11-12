# users/forms.py
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)

from .models import Usuario, empleado, empresa


class creacioUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'dni', 'telefono', 'foto')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class modificarUsuarioForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name','dni','telefono', 'foto' )

class EmpleadoForm(forms.ModelForm):
    fecha_ingreso = forms.DateField(
        input_formats=['%d-%m-%Y', '%d/%m/%Y'],
        widget=forms.DateInput(
            format='%d/%m/%Y', 
            attrs={
                'type': 'text', 
                'placeholder': 'dd/mm/aaaa',
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = empleado
        fields = ('fecha_ingreso', 'cargo', 'cv', 'experiencia')
        widgets = {  # noqa: RUF012
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'experiencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cv': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = empresa
        fields = ('nombre_empresa', 'descripcion', 'direccion', 'telefono', 'website')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'descripcion':
                field.widget.attrs['rows'] = '4'