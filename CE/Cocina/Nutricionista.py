from datetime import date

import MenuSemanal
import Platillo

class Nutricionista:

    #Falta heredar de clase Abstracta UsuarioEscolar
    
    def agregarRecomendacionesde(self, menu: MenuSemanal, platillo: Platillo, dia: date) -> None:
        menu.agregarPlatillo(platillo, dia)
    
    def eliminarRecomendacionesde(self, menu: MenuSemanal, platillo: Platillo, dia: date) -> None:
        menu.eliminarPlatillo(platillo, dia)
    
    def modificarRecomendacionesde(self, menu: MenuSemanal, platillo: Platillo, dia: date) -> None:
        menu.modificarPlatillo(platillo, dia)
    
    def crearMenu(self) -> MenuSemanal:
        print("Creando un nuevo menú semanal.")
        return MenuSemanal()

