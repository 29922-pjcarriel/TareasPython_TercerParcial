class Vehiculo:


    def __init__(self, cn):

        # Atributos privados de la matrícula
        self.__id = None
        self.__placa = None
        self.__marca = None
        self.__color = None
        self.__anio = None
        self.__avaluo = None

        # Guarda la conexión a la base de datos
        self.con = cn



    def get_list(self):

        html = """
        <h3 align="center">Lista de Vehículos</h3>

        <table border="1" cellpadding="6" cellspacing="0" align="center">
            <tr>
                <th colspan="7">Lista de Vehiculos</th>
            </tr>
            <tr>
                <th>Placa</th>
                <th>Marca</th>
                <th>Color</th>
                <th>Año</th>
                <th>Avalúo</th>
                <th colspan="3">Acciones</th>
            </tr>
        """

        sql = """
        SELECT v.id,
               v.placa,
               m.descripcion AS marca,
               c.descripcion AS color,
               v.anio,
               v.avaluo
        FROM vehiculo v, marca m, color c
        WHERE v.marca = m.id
          AND v.color = c.id
        """
        # Cursor con diccionarios
        cursor = self.con.cursor(dictionary=True)

        # Ejecuta la consulta
        cursor.execute(sql)

        # Recorre los registros
        for row in cursor.fetchall():

            # Debug tipo print_r()
            html += "<pre>" + print_r_py(row) + "</pre>"

            # Fila HTML
            html += f"""
            <tr>
                <td>{row['placa']}</td>
                <td>{row['marca']}</td>
                <td>{row['color']}</td>
                <td>{row['anio']}</td>
                <td>{row['avaluo']}</td>
                <td>BORRAR</td>
                <td>ACTUALIZAR</td>
                <td>DETALLE</td>
            </tr>
            """

        # Cierre de tabla
        html += "</table>"

        # Cierra cursor
        cursor.close()

        # Retorna HTML
        return html

    # -------------------------------
    # MENSAJE DE ERROR
    # -------------------------------
    def _message_error(self, tipo):
        return f"""
        <table border="0" align="center">
            <tr>
                <th>Error al {tipo}. Favor contactar a ..............</th>
            </tr>
            <tr>
                <th><a href="/">Regresar</a></th>
            </tr>
        </table>
        """


# -------------------------------
# FUNCIÓN AUXILIAR TIPO print_r()
# -------------------------------
def print_r_py(diccionario):

    salida = "Array\n(\n"

    for clave, valor in diccionario.items():
        salida += f"    [{clave}] => {valor}\n"

    salida += ")\n"

    return salida
