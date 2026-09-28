from django import forms
from .models import Publicacion, busquedaEmpleo, busquedaEmpleado

class PublicacionEmpresaForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        # Solo pedimos título y descripción. 
        # El autor lo pondremos nosotros por detrás según quién tenga la sesión iniciada.
        fields = ["oferta", "estado", "duracion", "urgencia", "lugar", "foto"]
    # --- MÉTODO PARA FILTRAR CAMPOS ---
    def __init__(self, *args, **kwargs):
        # 1. Atrapamos al 'usuario_actual' que enviamos desde la vista
        # Usamos pop() para sacarlo antes de que Django analice el resto de datos
        usuario = kwargs.pop('usuario_actual', None)
        
        # 2. Inicializamos el formulario de forma normal
        super().__init__(*args, **kwargs)
        
        # 3. Si atrapamos un usuario, filtramos el campo desplegable
        if usuario:
            # FILTRO:
            # 'oferta' es el nombre del campo en este form que queremos filtrar
            # La lógica de filter() -> buscamos en 'busquedaEmpleado' aquellos registros cuyo 'id_empresa' esté relacionado con el usuario actual
            self.fields['oferta'].queryset = busquedaEmpleado.objects.filter(id_empresa__usuario=usuario)
class PublicacionEmpleadoForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        # Solo pedimos título y descripción. 
        # El autor lo pondremos nosotros por detrás según quién tenga la sesión iniciada.
        fields = ["busqueda", "estado", "duracion", "urgencia", "lugar", "foto"]
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario_actual', None)
        
        super().__init__(*args, **kwargs)
        
        if usuario:
            self.fields['busqueda'].queryset = busquedaEmpleo.objects.filter(id_empleado__usuario=usuario)