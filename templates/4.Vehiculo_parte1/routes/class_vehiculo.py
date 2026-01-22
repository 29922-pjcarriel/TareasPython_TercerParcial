from datetime import datetime

class vehiculo:
    def __init__(self, cn):
        self.con = cn
        self.id = None
        self.placa = None
        self.marca = None
        self.motor = None
        self.chasis = None
        self.combustible = None
        self.anio = None
        self.color = None
        self.foto = None
        self.avaluo = None

    # =====================================================
    # FORMULARIO (equivalente a get_form() en PHP)
    # =====================================================
    def get_form(self, id=None):

        combustibles = [
            "Gasolina Extra",
            "Diesel",
            "Eléctrico",
            "EcoPais"
        ]

        html = f"""
        <form name="vehiculo" method="POST" action="" enctype="multipart/form-data">
            <table border="1" align="center">
                <tr>
                    <th colspan="2">DATOS VEHÍCULO</th>
                </tr>

                <tr>
                    <td>Placa:</td>
                    <td><input type="text" size="6" name="placa"></td>
                </tr>

                <tr>
                    <td>Marca:</td>
                    <td>{self._get_combo_db("marca", "id", "descripcion", "marcaCMB")}</td>
                </tr>

                <tr>
                    <td>Motor:</td>
                    <td><input type="text" size="15" name="motor"></td>
                </tr>

                <tr>
                    <td>Chasis:</td>
                    <td><input type="text" size="15" name="chasis"></td>
                </tr>

                <tr>
                    <td>Combustible:</td>
                    <td>{self._get_radio(combustibles, "combustibleRBT")}</td>
                </tr>

                <tr>
                    <td>Año:</td>
                    <td>{self._get_combo_anio("anio", 2000)}</td>
                </tr>

                <tr>
                    <td>Color:</td>
                    <td>{self._get_combo_db("color", "id", "descripcion", "colorCMB")}</td>
                </tr>

                <tr>
                    <td>Foto:</td>
                    <td><input type="file" name="foto"></td>
                </tr>

                <tr>
                    <td>Avalúo:</td>
                    <td><input type="text" size="8" name="avaluo"></td>
                </tr>

                <tr>
                    <th colspan="2">
                        <input type="submit" name="Guardar" value="GUARDAR">
                    </th>
                </tr>
            </table>
        </form>
        """
        return html

    # =====================================================
    # COMBO DESDE BD (marca / color)
    # =====================================================
    def _get_combo_db(self, tabla, valor, etiqueta, nombre):
        html = f'<select name="{nombre}">'
        cursor = self.con.cursor(dictionary=True)
        cursor.execute(f"SELECT {valor}, {etiqueta} FROM {tabla}")
        for row in cursor.fetchall():
            html += f'<option value="{row[valor]}">{row[etiqueta]}</option>'
        html += '</select>'
        cursor.close()
        return html

    # =====================================================
    # COMBO AÑOS
    # =====================================================
    def _get_combo_anio(self, nombre, anio_inicial):
        html = f'<select name="{nombre}">'
        anio_actual = datetime.now().year
        for i in range(anio_inicial, anio_actual + 1):
            html += f'<option value="{i}">{i}</option>'
        html += '</select>'
        return html

    # =====================================================
    # RADIO BUTTONS (combustible)
    # =====================================================
    def _get_radio(self, arreglo, nombre):
        html = '<table border="0" align="left">'
        for i, etiqueta in enumerate(arreglo):
            checked = 'checked' if i == 2 else ''
            html += f"""
            <tr>
                <td>{etiqueta}</td>
                <td>
                    <input type="radio" name="{nombre}" value="{etiqueta}" {checked}>
                </td>
            </tr>
            """
        html += '</table>'
        return html

    # =====================================================
    # LISTADO DE VEHÍCULOS
    # =====================================================
    def get_list(self):
        html = """
        <table border="1" align="center">
            <tr>
                <th colspan="8">Lista de Vehículos</th>
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

        cursor = self.con.cursor(dictionary=True)
        cursor.execute(sql)

        for row in cursor.fetchall():
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

        html += "</table>"
        cursor.close()
        return html

    # =====================================================
    # MENSAJE DE ERROR (equivalente a _message_error PHP)
    # =====================================================
    def _message_error(self, tipo):
        return f"""
        <table border="0" align="center">
            <tr>
                <th>Error al {tipo}. Favor contactar al administrador.</th>
            </tr>
            <tr>
                <th><a href="">Regresar</a></th>
            </tr>
        </table>
        """
