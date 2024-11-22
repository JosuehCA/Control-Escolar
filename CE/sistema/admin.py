from django.contrib import admin

from .models.models import *
from .models.models_mensajeria import *
from .models.models_reportes import *

admin.site.register(Platillo)
admin.site.register(MenuSemanal)
admin.site.register(Grupo)
admin.site.register(Actividad)


admin.site.register(ReporteGrupo)
admin.site.register(ReporteGlobal)


admin.site.register(UsuarioEscolar)
admin.site.register(GestorDeGrupos)
admin.site.register(Profesor)
admin.site.register(Tutor)
admin.site.register(Alumno)
admin.site.register(Nutricionista)


admin.site.register(MensajePrivado)
admin.site.register(MensajeGrupal)
admin.site.register(MensajeGeneral)
admin.site.register(Conversacion)
admin.site.register(Notificacion)