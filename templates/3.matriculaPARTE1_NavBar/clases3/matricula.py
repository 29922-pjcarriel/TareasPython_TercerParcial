# clases/matricula.py
# Replica directa de class/class.matricula.php (mismas funciones y misma lógica)
from __future__ import annotations
from typing import Optional

class Matricula:
    def __init__(self, cn):
        self.con = cn

    def get_form(self, _id: Optional[str] = None) -> str:
        html = f"""
        <form name="matricula" method="POST" action="">

            <table border="1" align="center">
                <tr><th colspan="2">DATOS MATRÍCULA</th></tr>

                <tr>
                    <td>Fecha:</td>
                    <td><input type="date" name="fecha"></td>
                </tr>

                <tr>
                    <td>Vehículo:</td>
                    <td>{self._get_combo_db("vehiculo","id","placa","vehiculoCMB")}</td>
                </tr>

                <tr>
                    <td>Agencia:</td>
                    <td>{self._get_combo_db("agencia","id","descripcion","agenciaCMB")}</td>
                </tr>

                <tr>
                    <td>Año:</td>
                    <td>{self._get_combo_anio("anio",2000)}</td>
                </tr>

                <tr>
                    <th colspan="2"><input type="submit" name="Guardar" value="GUARDAR"></th>
                </tr>
            </table>
        </form>
        """
        return html

    def _get_combo_db(self, tabla: str, valor: str, etiqueta: str, nombre: str) -> str:
        html = [f'<select name="{nombre}">']
        sql = f"SELECT {valor},{etiqueta} FROM {tabla};"
        cur = self._cursor()
        cur.execute(sql)

        for row in cur.fetchall():
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

    def get_list(self) -> str:
        html = ["""
        <table border="1" align="center">
            <tr><th colspan="6">Lista de Matrículas</th></tr>
            <tr>
                <th>Fecha</th>
                <th>Vehículo</th>
                <th>Agencia</th>
                <th>Año</th>
                <th colspan="3">Acciones</th>
            </tr>
        """]

        sql = (
            "SELECT m.id, m.fecha, v.placa as vehiculo, a.descripcion as agencia, m.anio "
            "FROM matricula m, vehiculo v, agencia a "
            "WHERE m.vehiculo = v.id AND m.agencia = a.id;"
        )
        cur = self._cursor()
        cur.execute(sql)

        for row in cur.fetchall():
            if isinstance(row, dict):
                fecha = row.get("fecha")
                vehiculo = row.get("vehiculo")
                agencia = row.get("agencia")
                anio = row.get("anio")
            else:
                _, fecha, vehiculo, agencia, anio = row[:5]
            html.append(f"""
                <tr>
                    <td>{fecha}</td>
                    <td>{vehiculo}</td>
                    <td>{agencia}</td>
                    <td>{anio}</td>
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
            <tr><th><a href="/matricula">Regresar</a></th></tr>
        </table>
        """

    def _cursor(self):
        try:
            return self.con.cursor(dictionary=True)
        except TypeError:
            pass
        try:
            import pymysql
            return self.con.cursor(pymysql.cursors.DictCursor)
        except Exception:
            return self.con.cursor()
