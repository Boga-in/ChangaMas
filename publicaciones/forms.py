from django import forms
from .models import Publicacion, Habilidad

class PublicacionForm(forms.ModelForm):
    # Campo opcional para escribir habilidades nuevas que no estén en las píldoras
    nuevas_habilidades = forms.CharField(
        max_length=200,
        required=False,
        label="¿No encontrás tu habilidad? Agregala acá",
        help_text="Separadas por coma.",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Durlock, Soldadura'})
    )

    class Meta:
        model = Publicacion
        # Incluimos 'habilidades'
        fields = ["titulo", "descripcion", "precio", "estado", "duracion", "urgencia", "lugar", "habilidades", "foto"]
        widgets = {
            'habilidades': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'habilidades':
                field.widget.attrs['class'] = 'form-control'
            if field_name == 'descripcion':
                field.widget.attrs['rows'] = '4'

    def save(self, commit=True):
        publicacion = super().save(commit=commit)
        
        # Procesamos las habilidades nuevas escritas a mano
        texto_nuevas = self.cleaned_data.get('nuevas_habilidades', '')
        if texto_nuevas:
            nombres = [n.strip().capitalize() for n in texto_nuevas.split(',') if n.strip()]
            habilidades_creadas = [Habilidad.objects.get_or_create(nombre=nom)[0] for nom in nombres]
            
            # Unimos las seleccionadas en las píldoras + las creadas a mano
            if commit:
                publicacion.habilidades.add(*habilidades_creadas)
                
        return publicacion