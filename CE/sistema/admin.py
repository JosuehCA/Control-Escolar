from django.contrib import admin

from .models import *

admin.site.register(Platillo)
admin.site.register(MenuPlatillo)
admin.site.register(MenuSemanal)
admin.site.register(Grupo)
admin.site.register(Actividad)


admin.site.register(ReporteAlumno)
admin.site.register(ReporteGrupo)
admin.site.register(ReporteGlobal)


admin.site.register(UsuarioEscolar)
admin.site.register(Administrador)
admin.site.register(Profesor)
admin.site.register(Tutor)
admin.site.register(Alumno)
admin.site.register(Nutricionista)


admin.site.register(MensajeDirecto)
admin.site.register(MensajeGrupo)
admin.site.register(MensajePlantel)
admin.site.register(Mensajero)
admin.site.register(Conversacion)
admin.site.register(Notificacion)