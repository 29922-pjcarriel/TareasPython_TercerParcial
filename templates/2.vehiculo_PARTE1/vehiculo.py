# vehiculo.py
from datetime import datetime

class Vehiculo:
    def __init__(self, con):
        self.con = con

    # =============== FORM (igual a PHP) ==================
    def get_form(self, _id=None):
        combustibles = [
            "Gasolina Extra",
            "Diesel",
            "Eléctrico",
            "EcoPais"
        ]

        html = f"""
        <form name="vehiculo" method="POST" action="/" enctype="multipart/form-data">
            <table border="1" align="center">
                <tr>
                    <th colspan="2">DATOS VEHÍCULO</th>
                </tr>
                <tr>
                    <td>Placa:</td>
                    <td><input type="text" size="6" name="placa" required></td>
                </tr>
                <tr>
                    <td>Marca:</td>
                    <td>{self._get_combo_db("marca","id","descripcion","marcaCMB")}</td>
                </tr>
                <tr>
                    <td>Motor:</td>
                    <td><input type="text" size="15" name="motor" required></td>
                </tr>
                <tr>
                    <td>Chasis:</td>
                    <td><input type="text" size="15" name="chasis" required></td>
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
                    <td>{self._get_combo_db("color","id","descripcion","colorCMB")}</td>
                </tr>
                <tr>
                    <td>Foto:</td>
                    <td><input type="file" name="foto" accept="image/*"></td>
                </tr>
                <tr>
                    <td>Avalúo:</td>
                    <td><input type="text" size="8" name="avaluo" required></td>
                </tr>
                <tr>
                    <th colspan="2"><input type="submit" name="Guardar" value="GUARDAR"></th>
                </tr>
            </table>
        </form>
        <div style="text-align:center; margin-top:10px;">
            <a href="/">Regresar</a>
        </div>
        """
        return html

    # =============== LIST (igual a PHP) ==================
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
        SELECT v.id, v.placa, m.descripcion AS marca, c.descripcion AS color, v.anio, v.avaluo
        FROM vehiculo v, color c, marca m
        WHERE v.marca=m.id AND v.color=c.id;
        """

        try:
            with self.con.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()

            for row in rows:
                html += f"""
                <tr>
                    <td>{row['placa']}</td>
                    <td>{row['marca']}</td>
                    <td>{row['color']}</td>
                    <td>{row['anio']}</td>
                    <td>{row['avaluo']}</td>

                    <!-- IGUAL QUE TU PHP: TEXTO EN <th>, SIN LINKS -->
                    <th>BORRAR</th>
                    <th>ACTUALIZAR</th>
                    <th>DETALLE</th>
                </tr>
                """

            html += "</table>"
            return html

        except Exception:
            return self._message_error("listar")

    # ================== GUARDAR (POST) ==================
    def insertar(self, data):
        sql = """
        INSERT INTO vehiculo
        (placa, marca, motor, chasis, combustible, anio, color, foto, avaluo)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            with self.con.cursor() as cur:
                cur.execute(sql, (
                    data["placa"],
                    data["marca"],
                    data["motor"],
                    data["chasis"],
                    data["combustible"],
                    int(data["anio"]),
                    data["color"],
                    data["foto"],
                    float(data["avaluo"]),
                ))
            self.con.commit()
            return True
        except Exception:
            self.con.rollback()
            return False

    # ================== HELPERS (igual a PHP) ==================
    def _get_combo_db(self, tabla, valor, etiqueta, nombre):
        html = f'<select name="{nombre}">'
        sql = f"SELECT {valor},{etiqueta} FROM {tabla};"
        try:
            with self.con.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
            for row in rows:
                html += f'<option value="{row[valor]}">{row[etiqueta]}</option>\n'
            html += "</select>"
            return html
        except Exception:
            return f'<select name="{nombre}"></select>'

    def _get_combo_anio(self, nombre, anio_inicial):
        html = f'<select name="{nombre}">'
        anio_actual = datetime.now().year
        for i in range(anio_inicial, anio_actual + 1):
            html += f'<option value="{i}">{i}</option>\n'
        html += "</select>"
        return html

    def _get_radio(self, arreglo, nombre):
        html = '<table border="0" align="left">'
        for i, etiqueta in enumerate(arreglo):
            checked = 'checked="checked"' if i == 2 else ""
            html += f"""
            <tr>
                <td>{etiqueta}</td>
                <td><input type="radio" value="{etiqueta}" name="{nombre}" {checked}/></td>
            </tr>
            """
        html += "</table>"
        return html

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
