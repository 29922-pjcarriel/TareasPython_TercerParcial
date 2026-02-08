class Notebook:
    def __init__(self, _id: int, marca: str, precio: float):
        self.id = _id
        self.marca = marca
        self.precio = float(precio)

    def getMarca(self):
        return self.marca

    def getPrecio(self):
        return self.precio
