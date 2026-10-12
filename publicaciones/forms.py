from django import forms
from .models import Publicacion, Habilidad

class PublicacionForm(forms.ModelForm):
    # 1. CREAMOS UN CAMPO DE TEXTO FANTASMA PARA QUE EL USUARIO ESCRIBA
    habilidades_texto = forms.CharField(
        max_length=200,
        required=False,
        label="Habilidades o Etiquetas",
        help_text="Escribí las habilidades separadas por comas (Ejemplo: Albañilería, Plomería, Pintura).",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Electricidad, Gasista, Durlock'})
    )

    class Meta:
        model = Publicacion
        # 2. SACAMOS 'habilidades' DE ACA, Y DEJAMOS EL RESTO
        fields = ["titulo", "descripcion", "precio", "estado", "duracion", "urgencia", "lugar", "foto"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inyectamos Bootstrap a todos los campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'descripcion':
                field.widget.attrs['rows'] = '4'
                
        # Si estamos EDITANDO una publicación, le precargamos las habilidades actuales como texto
        if self.instance and self.instance.pk:
            nombres = self.instance.habilidades.values_list('nombre', flat=True)
            self.fields['habilidades_texto'].initial = ", ".join(nombres)

    # 3. INTERCEPTAMOS EL GUARDADO PARA CREAR LAS ETIQUETAS
    def save(self, commit=True):
        # Guardamos la publicación primero (commit=False evita que se guarde en BBDD de inmediato)
        publicacion = super().save(commit=False)
        
        if commit:
            publicacion.save() # Guardamos la publicación para que tenga un ID
            self._save_m2m_habilidades(publicacion) # Guardamos las habilidades
            
        return publicacion

    def _save_m2m_habilidades(self, publicacion):
        # Agarramos el texto que escribió el usuario
        texto = self.cleaned_data.get('habilidades_texto', '')
        
        # Lo separamos por las comas, le quitamos espacios extra y lo ponemos con Mayúscula inicial
        nombres_habilidades = [n.strip().capitalize() for n in texto.split(',') if n.strip()]
        
        habilidades_objs = []
        for nombre in nombres_habilidades:
            # get_or_create: Busca si ya existe una habilidad con ese nombre. 
            # Si no existe, la crea mágicamente.
            obj, created = Habilidad.objects.get_or_create(nombre=nombre)
            habilidades_objs.append(obj)
            
        # Finalmente, enlazamos estas habilidades a nuestra publicación
        publicacion.habilidades.set(habilidades_objs)