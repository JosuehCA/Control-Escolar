class Platillo:
    def __init__(self, nombre: str, consideracionesMenu: list, descripcion: str):
        self.nombre = nombre
        self.consideracionesMenu = consideracionesMenu  
        self.descripcion = descripcion 

    # Getters
    def getNombre(self) -> str:
        return self.nombre
    
    def getConsideracionesMenu(self) -> list:
        return self.consideracionesMenu
    
    def getDescripcion(self) -> str:
        return self.descripcion

    # Setters
    def setNombre(self, nombre: str)-> None:
        self.nombre = nombre
    
    def setConsideracionesMenu(self, consideracionesMenu: list) -> None:
        self.consideracionesMenu = consideracionesMenu
    
    def setDescripcion(self, descripcion: str) -> None:
        self.descripcion = descripcion 

    '''
    def __str__(self):
        return f"Platillo: {self.nombre}, Descripción: {self.descripcion}, Consideraciones: {self.consideracionesMenu}"
    '''

