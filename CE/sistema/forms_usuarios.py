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
    
class ModificarUsuarioForm(forms.Form):
    
    nombre = forms.CharField(label="Nombres", max_length=100, required=True)
    apellido = forms.CharField(label="Apellidos", max_length=100, required=True)
    username = forms.CharField(label="Nombre de usuario", max_length=50, required=True)
    contrasena = forms.CharField(label="Contraseña", required=True)

    
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
    
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)  # Recibimos el usuario como argumento adicional
        super().__init__(*args, **kwargs)
        if usuario:
            # Inicializamos los valores de los campos con los datos del usuario
            self.fields['nombre'].initial = usuario.first_name
            self.fields['apellido'].initial = usuario.last_name
            self.fields['username'].initial = usuario.username
            # Opcional: No es común inicializar contraseñas por seguridad
            self.fields['grupo'].initial = getattr(usuario, 'grupo', None)  # Si el usuario tiene un grupo
            self.fields['tutor'].initial = getattr(usuario, 'tutorAlumno', None)  # Si el usuario tiene un tutor
            
        self.fields['nombre'].required = False  # El campo 'nombre' no será obligatorio
        self.fields['apellido'].required = False
        self.fields['username'].required = False
        self.fields['contrasena'].required = False
        