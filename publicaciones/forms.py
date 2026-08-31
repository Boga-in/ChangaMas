from django import forms
from .models import Publicacion

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        # Solo pedimos título y descripción. 
        # El autor lo pondremos nosotros por detrás según quién tenga la sesión iniciada.
        fields = ['titulo', 'descripcion']