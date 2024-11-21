from django import forms

from sistema.models.models import Grupo, Tutor, UsuarioEscolar


class CrearUsuarioForm(forms.Form):
    ROLES = [
        ('Profesor', 'Profesor'),
        ('Tutor', 'Tutor'),
        ('Alumno', 'Alumno'),
        ('Nutricionista', 'Nutricionista'),
    ]

    nombre = forms.CharField(label="Nombres", max_length=100, required=True)
    apellido = forms.CharField(label="Apellidos", max_length=100, required=True)
    username = forms.CharField(label="Nombre de usuario", max_length=50, required=True)
    contrasena = forms.CharField(label="Contraseña", required=True)
    rol = forms.ChoiceField(label="Tipo de usuario", choices=ROLES, required=True)
    
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        label="Grupo (solo para Profesores)",
        required=False
    )
    
    tutor = forms.ModelChoiceField(
        queryset=Tutor.objects.all(),
        label="Tutor (solo para Alumnos)",
        required=False
    )

    def clean(self):
        """
        Valida que los campos opcionales sean enviados según el rol seleccionado.
        """
        cleaned_data = super().clean()
        rol = cleaned_data.get('rol')
        
        if rol == 'Profesor' and not cleaned_data.get('grupo'):
            self.add_error('grupo', 'Debes seleccionar un grupo para el Profesor.')
        elif rol == 'Alumno' and not cleaned_data.get('tutor'):
            self.add_error('tutor', 'Debes seleccionar un tutor para el Alumno.')

        return cleaned_data

class EliminarUsuarioForm(forms.Form):
    usuarios = forms.ModelMultipleChoiceField(
        queryset=UsuarioEscolar.objects.all(),  
        widget=forms.CheckboxSelectMultiple,  # Usa checkboxes para selección múltiple
        required=True,  # Obliga a seleccionar al menos un grupo
        label="Selecciona Usuarios para eliminar"
    )