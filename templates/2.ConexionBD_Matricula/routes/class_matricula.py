class Matricula:

    # Constructor: se ejecuta cuando se crea un objeto Matricula
    # Recibe la conexión a la base de datos
    def __init__(self, cn):

        # Atributos privados de la matrícula
        self.__id = None
        self.__fecha = None
        self.__vehiculo = None
        self.__agencia = None
        self.__anio = None

        # Guarda la conexión a la base de datos
        self.con = cn


    # -------------------------------
    # LISTAR MATRÍCULAS
    # -------------------------------
    def get_list(self):

        # HTML inicial de la tabla
        html = """
        <table border="1" align="center">
            <tr>
                <th colspan="7">Lista de Matrículas</th>
            </tr>
            <tr>
                <th>Fecha</th>
                <th>Vehículo</th>
                <th>Agencia</th>
                <th>Año</th>
                <th colspan="3">Acciones</th>
            </tr>
        """

        # Consulta SQL
        # Se asume:
        # - vehiculo hace referencia a la tabla vehiculo
        # - agencia hace referencia a la tabla agencia
        sql = """
        SELECT m.id,
               m.fecha,
               v.placa AS vehiculo,
               a.descripcion AS agencia,
               m.anio
        FROM matricula m, vehiculo v, agencia a
        WHERE m.vehiculo = v.id
          AND m.agencia = a.id
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
                <td>{row['fecha']}</td>
                <td>{row['vehiculo']}</td>
                <td>{row['agencia']}</td>
                <td>{row['anio']}</td>
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
