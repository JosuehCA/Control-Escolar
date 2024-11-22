from django.db import models as m
from django.conf import settings
from sistema.models.models import UsuarioEscolar, Grupo
from abc import abstractmethod
from django.db.models import Q

class MensajeBase(m.Model):
    """TDA Mensaje. Define la estructura de un mensaje dentro del mensajero virtual."""

    emisorUsuario = m.ForeignKey(UsuarioEscolar, on_delete=m.CASCADE)
    contenidoMensaje = m.CharField(max_length=2000)
    fechaEnviado = m.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Representación en cadena de un mensaje."""
        return f"Mensaje de {self.emisorUsuario} enviado en {self.fechaEnviado}"

    def almacenarEnBaseDeDatos(self) -> None:
        """Almacena el mensaje en la base de datos."""
        self.save()

    @abstractmethod
    def recibirDatosDeMensajeEnDiccionario(self, datosDeMensaje: dict) -> None:
        """Recibe los datos de un mensaje en formato JSON."""
        pass

    class Meta:
        abstract = True



class MensajePrivado(MensajeBase):
    """TDA Mensaje Directo. Particulariza un mensaje de manera individual."""
    receptorUsuario = m.ForeignKey(UsuarioEscolar, on_delete=m.DO_NOTHING, related_name="receptor")
    
    def receptorEsDistintoDeEmisor(self, emisor: UsuarioEscolar, receptor: UsuarioEscolar) -> bool:
        """
        Verifica si el mensaje es válido para ser enviado, asegurando que el emisor y receptor sean distintos.
        """
        return emisor != receptor
    
    @classmethod
    def obtenerMensajesEntreUsuarios(cls, usuarioEmisor: UsuarioEscolar, usuarioReceptor: UsuarioEscolar) -> m.QuerySet:
        """Obtiene los mensajes filtrados que fueron enviados a un usuario específico."""
        return cls.objects.filter(Q(emisorUsuario=usuarioEmisor, receptorUsuario=usuarioReceptor) | Q(emisorUsuario=usuarioReceptor, receptor=usuarioEmisor)).order_by('fechaEnviado')
    
    def __str__(self) -> str:
        """Representación en cadena de un mensaje directo."""
        return f"Mensaje directo de {self.emisorUsuario} a {self.receptorUsuario}"
    
    def recibirDatosDeMensajeEnDiccionario(self, datosDeMensaje: dict) -> None:
        """Recibe los datos de un mensaje privado en formato JSON."""
        self.emisorUsuario = datosDeMensaje['emisorUsuario']
        self.receptorUsuario = datosDeMensaje['receptorUsuario']
        self.contenidoMensaje = datosDeMensaje['contenidoMensaje']
    
    class Meta:
        verbose_name = "Mensaje Directo"
        verbose_name_plural = "Mensajes: Directos"



class MensajeGrupal(MensajeBase):
    """TDA Mensaje de Grupo. Particulariza un mensaje de manera grupal."""

    grupoRelacionado = m.ForeignKey(Grupo, on_delete=m.DO_NOTHING, related_name="mensajes")

    @classmethod
    def obtenerMensajesDeGrupo(cls, grupo: Grupo) -> m.QuerySet:
        """Obtiene los mensajes filtrados que fueron enviados a un grupo específico."""
        return cls.objects.filter(grupoRelacionado=grupo).order_by('fechaEnviado')
    
    def recibirDatosDeMensajeEnDiccionario(self, datosDeMensaje: dict) -> None:
        """Recibe los datos de un mensaje grupal en formato JSON."""
        self.emisorUsuario = datosDeMensaje['emisorUsuario']
        self.contenidoMensaje = datosDeMensaje['contenidoMensaje']
        self.grupoRelacionado = datosDeMensaje['grupoRelacionado']

    def __str__(self) -> str:
        """Representación en cadena de un mensaje grupal."""
        return f"Mensaje grupal de {self.emisorUsuario} en {self.grupoRelacionado}, contenido: {self.contenidoMensaje}, fecha: {self.fechaEnviado}"

    class Meta:
        verbose_name = "Mensaje Grupo"
        verbose_name_plural = "Mensajes: Grupos"



class MensajeGeneral(MensajeBase):
    """TDA Mensaje Plantel. Establece un mensaje compartido de manera global a todo el plantel."""

    @classmethod
    def obtenerMensajesGenerales(cls) -> m.QuerySet:
        """Obtiene los mensajes filtrados que fueron enviados a todo el plantel."""
        return cls.objects.all().order_by('fechaEnviado')

    def recibirDatosDeMensajeEnDiccionario(self, datosDeMensaje: dict) -> None:
        """Recibe los datos de un mensaje general en formato JSON."""
        self.emisorUsuario = datosDeMensaje['emisorUsuario']
        self.contenidoMensaje = datosDeMensaje['contenidoMensaje']

    def __str__(self) -> str:
        """Representación en cadena de un mensaje general."""
        return f"Mensaje general de {self.emisorUsuario} en {self.fechaEnviado}, contenido: {self.contenidoMensaje}"

    class Meta:
        verbose_name = "Mensaje General"
        verbose_name_plural = "Mensajes: Generales"