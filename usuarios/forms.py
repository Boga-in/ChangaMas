# users/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Usuario
from .models import empleado

class creacioUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        # Añadimos los campos que queremos que se muestren en el formulario de creación
        fields = ('username', 'email', 'first_name', 'last_name','dni','telefono', 'foto' )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Recorre todos los campos y les agrega la clase de Bootstrap
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'

class modificarUsuarioForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name','dni','telefono', 'foto' )

class EmpleadoForm(forms.ModelForm):
    # 1. Sobrescribes el campo aquí arriba para indicarle qué formatos aceptas
    fecha_ingreso = forms.DateField(
        input_formats=['%d-%m-%Y', '%d/%m/%Y'], # Acepta con guiones o barras
        widget=forms.DateInput(
            # 2. Obligas al widget a mostrarlo en este formato
            format='%d-%m-%Y', 
            attrs={

                'type': 'text', 
                'placeholder': 'dd-mm-aaaa',
                'class': 'form-control'
            }
        )
    )
    class Meta:
        model = empleado
        fields = ['usuario', 'fecha_ingreso', 'cargo', 'cv', 'experiencia']

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'