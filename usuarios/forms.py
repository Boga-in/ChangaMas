# users/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario

class creacioUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        # Añade los campos extra que necesites
        fields = ('username', 'email', 'first_name', 'last_name','dni','telefono', 'foto' )

class modificarUsuarioForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name','dni','telefono', 'foto' )