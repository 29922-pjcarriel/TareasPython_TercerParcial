# clases/vehiculo.py
# Replica directa de class/class.vehiculo.php (mismas funciones y misma lógica)
from __future__ import annotations
from typing import Any, Dict, List, Optional

class Vehiculo:
    def __init__(self, cn):
        self.con = cn

    def get_form(self, _id: Optional[str] = None) -> str:
        combustibles = ["Gasolina Extra", "Diesel", "Eléctrico", "EcoPais"]

        html = f"""
        <form name="vehiculo" method="POST" action="" enctype="multipart/form-data">

            <table border="1" align="center">
                <tr><th colspan="2">DATOS VEHÍCULO</th></tr>
                <tr>
                    <td>Placa:</td>
                    <td><input type="text" size="6" name="placa"></td>
                </tr>
                <tr>
                    <td>Marca:</td>
                    <td>{self._get_combo_db("marca","id","descripcion","marcaCMB")}</td>
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
                    <td>{self._get_combo_db("color","id","descripcion","colorCMB")}</td>
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
                    <th colspan="2"><input type="submit" name="Guardar" value="GUARDAR"></th>
                </tr>
            </table>
        </form>
        """
        return html

    # $this->_get_combo_db("marca","id","descripcion","marcaCMB")
    def _get_combo_db(self, tabla: str, valor: str, etiqueta: str, nombre: str) -> str:
        html = [f'<select name="{nombre}">']
        sql = f"SELECT {valor},{etiqueta} FROM {tabla};"
        cur = self._cursor()
        cur.execute(sql)
        for row in cur.fetchall():
            # soporta dict o tuple
            if isinstance(row, dict):
                v = row.get(valor)
                e = row.get(etiqueta)
            else:
                v, e = row[0], row[1]
            html.append(f'<option value="{v}">{e}</option>')
        html.append("</select>")
        cur.close()
        return "\n".join(html)

    def _get_combo_anio(self, nombre: str, anio_inicial: int) -> str:
        from datetime import datetime
        anio_actual = datetime.now().year
        html = [f'<select name="{nombre}">']
        for i in range(anio_inicial, anio_actual + 1):
            html.append(f'<option value="{i}">{i}</option>')
        html.append("</select>")
        return "\n".join(html)

    # $this->_get_radio($combustibles, "combustibleRBT")
    def _get_radio(self, arreglo: List[str], nombre: str) -> str:
        html = ['<table border="0" align="left">']
        for i, etiqueta in enumerate(arreglo):
            checked = "checked" if i == 2 else ""
            html.append(f"""
            <tr>
                <td>{etiqueta}</td>
                <td><input type="radio" value="{etiqueta}" name="{nombre}" {checked}/></td>
            </tr>
            """)
        html.append("</table>")
        return "\n".join(html)

    def get_list(self) -> str:
        html = ["""
        <table border="1" align="center">
            <tr><th colspan="8">Lista de Vehículos</th></tr>
            <tr>
                <th>Placa</th>
                <th>Marca</th>
                <th>Color</th>
                <th>Año</th>
                <th>Avalúo</th>
                <th colspan="3">Acciones</th>
            </tr>
        """]

        sql = ("SELECT v.id, v.placa, m.descripcion as marca, c.descripcion as color, "
               "v.anio, v.avaluo "
               "FROM vehiculo v, color c, marca m "
               "WHERE v.marca=m.id AND v.color=c.id;")
        cur = self._cursor()
        cur.execute(sql)
        for row in cur.fetchall():
            if isinstance(row, dict):
                placa = row.get("placa")
                marca = row.get("marca")
                color = row.get("color")
                anio = row.get("anio")
                avaluo = row.get("avaluo")
            else:
                # fallback por posición
                _, placa, marca, color, anio, avaluo = row[:6]
            html.append(f"""
                <tr>
                    <td>{placa}</td>
                    <td>{marca}</td>
                    <td>{color}</td>
                    <td>{anio}</td>
                    <td>{avaluo}</td>
                    <td>BORRAR</td>
                    <td>ACTUALIZAR</td>
                    <td>DETALLE</td>
                </tr>
            """)
        cur.close()
        html.append("</table>")
        return "\n".join(html)

    def _message_error(self, tipo: str) -> str:
        return f"""
        <table border="0" align="center">
            <tr><th>Error al {tipo}. Favor contactar a ..............</th></tr>
            <tr><th><a href="/">Regresar</a></th></tr>
        </table>
        """

    def _cursor(self):
        """
        Cursor tipo dict si el driver lo soporta.
        - mysql-connector-python: cursor(dictionary=True)
        - pymysql: cursor(pymysql.cursors.DictCursor)
        """
        # mysql-connector-python
        try:
            return self.con.cursor(dictionary=True)
        except TypeError:
            pass
        # pymysql
        try:
            import pymysql
            return self.con.cursor(pymysql.cursors.DictCursor)
        except Exception:
            return self.con.cursor()
