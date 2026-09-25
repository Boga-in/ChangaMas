# users/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Usuario
from .models import empleado

class creacioUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        # Añade los campos extra que necesites
        fields = ('username', 'email', 'first_name', 'last_name','dni','telefono', 'foto' )

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
                # OJO: Si usas 'type': 'date', HTML5 ignora tu formato y usa 
                # el formato local del navegador (ej. mm/dd/yyyy en EEUU).
                # Para forzar tu formato exacto, usa 'text' y un placeholder.
                'type': 'text', 
                'placeholder': 'dd-mm-aaaa',
                'class': 'form-control' # Opcional, si usas Bootstrap
            }
        )
    )
    class Meta:
        model = empleado
        fields = ['usuario', 'fecha_ingreso', 'cargo', 'cv', 'experiencia']