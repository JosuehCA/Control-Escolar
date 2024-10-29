from datetime import date
from typing import Dict, List

from Platillo import Platillo

#PENDIENTE
class MenuSemanal:
    def __init__(self):
        self.opcionesDePlatillo: Dict[date, List[Platillo]] = {}
    
    def agregarPlatillo(self, platillo: Platillo, dia: date) -> None:
        if dia not in self.opcionesDePlatillo:
            self.opcionesDePlatillo[dia] = []
        self.opcionesDePlatillo[dia].append(platillo)
        print(f"Platillo agregado: {platillo.nombre} en el día {dia}")

    def eliminarPlatillo(self, platillo: Platillo, dia: date) -> None:
        if dia in self.opcionesDePlatillo:
            self.opcionesDePlatillo[dia] = [
                platilloExistente for platilloExistente in self.opcionesDePlatillo[dia] 
                if platilloExistente.nombre != platillo.nombre
            ]
            print(f"Platillo eliminado: {platillo.nombre} en el día {dia}")
        else:
            print("No hay platillos para este día.")

    
    def modificarPlatillo(self, platillo: Platillo, dia: date) -> None:
        if dia in self.opcionesDePlatillo:
            for indicePLatillo, platilloExistente in enumerate(self.opcionesDePlatillo[dia]):
                if platilloExistente.nombre == platillo.nombre:
                    self.opcionesDePlatillo[dia][indicePLatillo] = platillo
                    print(f"Platillo editado: {platillo.nombre} en el día {dia}")
                    return
        print("Platillo no encontrado para editar.")
    
    
    def visualizarPlatillo(self, dia: date) -> None:
        if dia in self.opcionesDePlatillo:
            print(f"Menú para el día {dia}:")
            for platillo in self.opcionesDePlatillo[dia]:
                print(f"  - {platillo}")
        else:
            print(f"No hay menú para el día {dia}.")
