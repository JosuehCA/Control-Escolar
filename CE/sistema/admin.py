from django.contrib import admin

from .models import *

admin.site.register(Menu)
admin.site.register(Salon)

admin.site.register(ReporteAlumno)
admin.site.register(ReporteSalon)
admin.site.register(ReporteGlobal)


admin.site.register(Usuario)
admin.site.register(Administrador)
admin.site.register(Profesor)
admin.site.register(Tutor)
admin.site.register(Alumno)
admin.site.register(Nutricionista)



admin.site.register(MensajeDirecto)
admin.site.register(MensajeSalon)
admin.site.register(MensajeAnuncio)
admin.site.register(Conversacion)
admin.site.register(Notificacion)