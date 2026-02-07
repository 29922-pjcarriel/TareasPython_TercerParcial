from dataclasses import dataclass

@dataclass
class Notebook:
    codigo: str
    marca: str
    precio: float

class NotebookCatalog:
    def __init__(self):
        self._data = {
            1: Notebook(codigo="NB-001", marca="HP", precio=650.00),
            2: Notebook(codigo="NB-002", marca="DELL", precio=720.00),
            3: Notebook(codigo="NB-003", marca="LENOVO", precio=590.00),
            4: Notebook(codigo="NB-004", marca="ASUS", precio=810.00),
        }

    def get_all(self):
        return self._data

    def get_by_marca(self, marca: str):
        if not marca:
            return None
        for obj in self._data.values():
            if obj.marca.lower() == marca.lower():
                return obj
        return None
