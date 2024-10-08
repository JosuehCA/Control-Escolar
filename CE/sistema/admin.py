from django.contrib import admin

from .models import *

admin.site.register(Menu)
admin.site.register(Grupo)
admin.site.register(Plato)
admin.site.register(Actividad)


admin.site.register(Reporte)
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
admin.site.register(MensajeAnuncio)
admin.site.register(Mensajero)
admin.site.register(Conversacion)
admin.site.register(Notificacion)