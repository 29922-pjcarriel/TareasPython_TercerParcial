# routes/class_vehiculo.py
# CLON FUNCIONAL DEL class.vehiculo.php
# CRUD COMPLETO + BD REAL + FK CONTROLADA

import base64
from datetime import datetime
from urllib.parse import quote_plus


class Vehiculo:

    # =====================================================
    # CONSTRUCTOR
    # =====================================================
    def __init__(self, cn):
        self.con = cn
        print("EJECUTANDOSE EL CONSTRUCTOR VEHICULO<br><br>")

    # =====================================================
    # BASE64 PARA ?d=
    # =====================================================
    def _b64(self, txt):
        return quote_plus(
            base64.b64encode(txt.encode("utf-8")).decode("utf-8")
        )

    # =====================================================
    # FORMULARIO (NEW / UPDATE)
    # =====================================================
    def get_form(self, id=None):

        if id is None or id == 0:
            row = {
                "placa": "", "marca": "", "motor": "",
                "chasis": "", "combustible": "",
                "anio": "", "color": "", "foto": "",
                "avaluo": ""
            }
            op = "new"
            flag = ""

        else:
            cur = self.con.cursor(dictionary=True)
            cur.execute("SELECT * FROM vehiculo WHERE id=%s", (id,))
            row = cur.fetchone()

            if row is None:
                return self._message_error(
                    f"tratar de actualizar el vehiculo con id= {id}<br>"
                )

            print("<br>REGISTRO A MODIFICAR:<br><pre>")
            print(row)
            print("</pre>")

            op = "update"
            flag = "enabled"

        combustibles = ["Gasolina", "Diesel", "Eléctrico"]

        return f"""
        <form method="POST" action="?" enctype="multipart/form-data">
            <input type="hidden" name="id" value="{id or 0}">
            <input type="hidden" name="op" value="{op}">
            <input type="hidden" name="foto_actual" value="{row['foto']}">

            <table border="2" align="center">
                <tr><th colspan="2">DATOS VEHÍCULO</th></tr>

                <tr><td>Placa:</td>
                    <td><input type="text" name="placa" value="{row['placa']}"></td></tr>

                <tr><td>Marca:</td>
                    <td>{self._get_combo_db("marca","id","descripcion","marca",row["marca"])}</td></tr>

                <tr><td>Motor:</td>
                    <td><input type="text" name="motor" value="{row['motor']}"></td></tr>

                <tr><td>Chasis:</td>
                    <td><input type="text" name="chasis" value="{row['chasis']}"></td></tr>

                <tr><td>Combustible:</td>
                    <td>{self._get_radio(combustibles,"combustible",row["combustible"])}</td></tr>

                <tr><td>Año:</td>
                    <td>{self._get_combo_anio("anio",1950,row["anio"])}</td></tr>

                <tr><td>Color:</td>
                    <td>{self._get_combo_db("color","id","descripcion","color",row["color"])}</td></tr>

                <tr><td>Foto:</td>
                    <td><input type="file" name="foto" {flag}></td></tr>

                <tr><td>Avalúo:</td>
                    <td><input type="text" name="avaluo" value="{row['avaluo']}" {flag}></td></tr>

                <tr><th colspan="2">
                    <input type="submit" name="Guardar" value="GUARDAR">
                </th></tr>
            </table>
        </form>
        """

    # =====================================================
    # GUARDAR (INSERT / UPDATE)
    # =====================================================
    def save_vehiculo(self, data, files):

        cur = self.con.cursor()
        foto_nombre = data.get("foto_actual", "")

        if files and "foto" in files and files["foto"].filename:
            foto = files["foto"]
            foto_nombre = foto.filename
            foto.save(f"images/{foto_nombre}")

        if data["op"] == "new":
            cur.execute("""
                INSERT INTO vehiculo
                (placa, marca, motor, chasis, combustible, anio, color, foto, avaluo)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                data["placa"], data["marca"], data["motor"],
                data["chasis"], data["combustible"],
                data["anio"], data["color"], foto_nombre,
                data["avaluo"]
            ))
            self.con.commit()
            return self._message_ok("insertó")

        if data["op"] == "update":
            cur.execute("""
                UPDATE vehiculo SET
                    placa=%s, marca=%s, motor=%s, chasis=%s,
                    combustible=%s, anio=%s, color=%s,
                    foto=%s, avaluo=%s
                WHERE id=%s
            """, (
                data["placa"], data["marca"], data["motor"],
                data["chasis"], data["combustible"],
                data["anio"], data["color"], foto_nombre,
                data["avaluo"], data["id"]
            ))
            self.con.commit()
            return self._message_ok("actualizó")

    # =====================================================
    # LISTA
    # =====================================================
    def get_list(self):

        html = f"""
        <table border="1" align="center">
            <tr><th colspan="8">Lista de Vehículos</th></tr>
            <tr><th colspan="8">
                <a href="?d={self._b64('new/0')}">Nuevo</a>
            </th></tr>
            <tr>
                <th>Placa</th><th>Marca</th><th>Color</th>
                <th>Año</th><th>Avalúo</th>
                <th colspan="3">Acciones</th>
            </tr>
        """

        cur = self.con.cursor(dictionary=True)
        cur.execute("""
            SELECT v.id, v.placa,
                   m.descripcion AS marca,
                   c.descripcion AS color,
                   v.anio, v.avaluo
            FROM vehiculo v, marca m, color c
            WHERE v.marca=m.id AND v.color=c.id
        """)

        for r in cur.fetchall():
            html += f"""
            <tr>
                <td>{r['placa']}</td>
                <td>{r['marca']}</td>
                <td>{r['color']}</td>
                <td>{r['anio']}</td>
                <td>{r['avaluo']}</td>
                <td><a href="?d={self._b64(f'del/{r["id"]}')}">Borrar</a></td>
                <td><a href="?d={self._b64(f'act/{r["id"]}')}">Actualizar</a></td>
                <td><a href="?d={self._b64(f'det/{r["id"]}')}">Detalle</a></td>
            </tr>
            """

        html += "</table>"
        return html

    # =====================================================
    # DETALLE (CON MATRÍCULA + IMAGEN)
    # =====================================================
    def get_detail_vehiculo(self, id):

        cur = self.con.cursor(dictionary=True)
        cur.execute("""
            SELECT v.placa, m.descripcion AS marca,
                   v.motor, v.chasis, v.combustible,
                   v.anio, c.descripcion AS color,
                   v.foto, v.avaluo
            FROM vehiculo v, marca m, color c
            WHERE v.id=%s AND v.marca=m.id AND v.color=c.id
        """, (id,))

        row = cur.fetchone()

        if row is None:
            return self._message_error(
                f"desplegar el detalle del vehiculo con id= {id}<br>"
            )

        return f"""
        <table border="1" align="center">
            <tr><th colspan="2">DATOS DEL VEHÍCULO</th></tr>

            <tr><td>Placa:</td><td>{row['placa']}</td></tr>
            <tr><td>Marca:</td><td>{row['marca']}</td></tr>
            <tr><td>Motor:</td><td>{row['motor']}</td></tr>
            <tr><td>Chasis:</td><td>{row['chasis']}</td></tr>
            <tr><td>Combustible:</td><td>{row['combustible']}</td></tr>
            <tr><td>Año:</td><td>{row['anio']}</td></tr>
            <tr><td>Color:</td><td>{row['color']}</td></tr>

            <tr><td>Avalúo:</td><th>${row['avaluo']} USD</th></tr>

            <tr>
                <td>Valor Matrícula:</td>
                <th>${self._calculo_matricula(row['avaluo'])} USD</th>
            </tr>

            <tr>
                <th colspan="2">
                    <img src="images/{row['foto']}" width="300px"/>
                </th>
            </tr>

            <tr><th colspan="2"><a href="?">Regresar</a></th></tr>
        </table>
        """

    # =====================================================
    # BORRAR (RESPETA FK)
    # =====================================================
    def delete_vehiculo(self, id):

        cur = self.con.cursor(dictionary=True)

        # Verificar matrículas asociadas
        cur.execute("SELECT COUNT(*) AS total FROM matricula WHERE vehiculo=%s", (id,))
        r = cur.fetchone()

        if r["total"] > 0:
            return self._message_error(
                "eliminar el vehículo porque tiene matrículas registradas.<br>"
            )

        cur.execute("DELETE FROM vehiculo WHERE id=%s", (id,))
        self.con.commit()

        return self._message_ok("eliminó")

    # =====================================================
    # UTILIDADES
    # =====================================================
    def _calculo_matricula(self, avaluo):
        try:
            return f"{float(avaluo) * 0.10:.2f}"
        except:
            return "0.00"

    def _get_combo_db(self, tabla, valor, etiqueta, nombre, defecto):
        html = f'<select name="{nombre}">'
        cur = self.con.cursor(dictionary=True)
        cur.execute(f"SELECT {valor},{etiqueta} FROM {tabla}")
        for r in cur.fetchall():
            sel = "selected" if r[valor] == defecto else ""
            html += f'<option value="{r[valor]}" {sel}>{r[etiqueta]}</option>'
        html += "</select>"
        return html

    def _get_combo_anio(self, nombre, inicio, defecto):
        html = f'<select name="{nombre}">'
        actual = datetime.now().year
        for i in range(inicio, actual + 1):
            sel = "selected" if i == defecto else ""
            html += f'<option value="{i}" {sel}>{i}</option>'
        html += "</select>"
        return html

    def _get_radio(self, arr, nombre, defecto):
        html = "<table>"
        for v in arr:
            chk = "checked" if v == defecto else ""
            html += f"""
            <tr>
                <td>{v}</td>
                <td><input type="radio" name="{nombre}" value="{v}" {chk}></td>
            </tr>
            """
        html += "</table>"
        return html

    # =====================================================
    # MENSAJES
    # =====================================================
    def _message_error(self, txt):
        return f"""
        <table align="center">
            <tr><th>Error al {txt}Favor contactar a ....................</th></tr>
            <tr><th><a href="?">Regresar</a></th></tr>
        </table>
        """

    def _message_ok(self, txt):
        return f"""
        <table align="center">
            <tr><th>El registro se {txt} correctamente</th></tr>
            <tr><th><a href="?">Regresar</a></th></tr>
        </table>
        """
