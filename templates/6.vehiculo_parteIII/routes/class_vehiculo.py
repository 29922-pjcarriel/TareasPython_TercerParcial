# routes/class_vehiculo.py

import base64
from datetime import datetime
from urllib.parse import quote_plus
from flask import current_app


# =========================================================
# BASE PATH DINÁMICO (CLAVE PARA EL MENÚ)
# =========================================================
def base_path():
    """
    Si el proyecto corre dentro del menú lanzador,
    BASE_PATH será algo como: /vehiculo_PARTE_II/app.py
    Si corre solo, será ""
    """
    return current_app.config.get("BASE_PATH", "")


class Vehiculo:

    def __init__(self, cn):
        self.con = cn
        print("EJECUTANDOSE EL CONSTRUCTOR VEHICULO<br><br>")

        # ATRIBUTOS (IGUAL QUE PHP)
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

    # =========================================================
    # HELPER BASE64 (IGUAL CONCEPTO PHP, PERO SEGURO EN URL)
    # =========================================================
    def _b64_url(self, texto):
        return quote_plus(
            base64.b64encode(texto.encode("utf-8")).decode("utf-8")
        )

    # =========================================================
    # FORMULARIO (NEW / UPDATE)
    # =========================================================
    def get_form(self, id=None):

        # Código agregado -- //
        if (id is None) or (id == 0):
            self.placa = None
            self.marca = None
            self.motor = None
            self.chasis = None
            self.combustible = None
            self.anio = None
            self.color = None
            self.foto = None
            self.avaluo = None

            flag = ""
            op = "new"
            bandera = 1

        else:
            cursor = self.con.cursor(dictionary=True)
            sql = f"SELECT * FROM vehiculo WHERE id={id};"
            cursor.execute(sql)
            row = cursor.fetchone()

            # VERIFICA SI EXISTE id
            bandera = 0 if row is None else 1

            if not bandera:
                mensaje = f"tratar de actualizar el vehiculo con id= {id} <br>"
                return self._message_error(mensaje)

            print("<br>REGISTRO A MODIFICAR:<br><pre>")
            print(row)
            print("</pre>")

            # ATRIBUTOS DE LA CLASE VEHICULO
            self.placa = row["placa"]
            self.marca = row["marca"]
            self.motor = row["motor"]
            self.chasis = row["chasis"]
            self.combustible = row["combustible"]
            self.anio = row["anio"]
            self.color = row["color"]
            self.foto = row["foto"]
            self.avaluo = row["avaluo"]

            flag = "enabled"
            op = "update"

        if bandera:

            combustibles = ["Gasolina", "Diesel", "Eléctrico"]

            html = f"""
            <form name="Form_vehiculo" method="POST"
                  action="{base_path()}/"
                  enctype="multipart/form-data">

                <input type="hidden" name="id" value="{id or 0}">
                <input type="hidden" name="op" value="{op}">

                <table border="2" align="center">
                    <tr>
                        <th colspan="2">DATOS VEHÍCULO</th>
                    </tr>
                    <tr>
                        <td>Placa:</td>
                        <td><input type="text" size="6" name="placa" value="{self.placa or ''}"></td>
                    </tr>
                    <tr>
                        <td>Marca:</td>
                        <td>{self._get_combo_db("marca","id","descripcion","marca",self.marca)}</td>
                    </tr>
                    <tr>
                        <td>Motor:</td>
                        <td><input type="text" size="15" name="motor" value="{self.motor or ''}"></td>
                    </tr>
                    <tr>
                        <td>Chasis:</td>
                        <td><input type="text" size="15" name="chasis" value="{self.chasis or ''}"></td>
                    </tr>
                    <tr>
                        <td>Combustible:</td>
                        <td>{self._get_radio(combustibles, "combustible", self.combustible)}</td>
                    </tr>
                    <tr>
                        <td>Año:</td>
                        <td>{self._get_combo_anio("anio",1950,self.anio)}</td>
                    </tr>
                    <tr>
                        <td>Color:</td>
                        <td>{self._get_combo_db("color","id","descripcion","color",self.color)}</td>
                    </tr>
                    <tr>
                        <td>Foto:</td>
                        <td><input type="file" name="foto" {flag}></td>
                    </tr>
                    <tr>
                        <td>Avalúo:</td>
                        <td><input type="text" size="8" name="avaluo" value="{self.avaluo or ''}" {flag}></td>
                    </tr>
                    <tr>
                        <th colspan="2"><input type="submit" name="Guardar" value="GUARDAR"></th>
                    </tr>
                </table>
            </form>
            """
            return html

    # =========================================================
    # LISTADO
    # =========================================================
    def get_list(self):

        d_new = self._b64_url("new/0")

        html = f"""
        <table border="1" align="center">
            <tr>
                <th colspan="8">Lista de Vehículos</th>
            </tr>
            <tr>
                <th colspan="8"><a href="{base_path()}/?d={d_new}">Nuevo</a></th>
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
        SELECT v.id, v.placa, m.descripcion AS marca,
               c.descripcion AS color, v.anio, v.avaluo
        FROM vehiculo v, color c, marca m
        WHERE v.marca=m.id AND v.color=c.id;
        """

        cursor = self.con.cursor(dictionary=True)
        cursor.execute(sql)
        rows = cursor.fetchall()

        if len(rows) != 0:
            for row in rows:

                d_del = self._b64_url(f"del/{row['id']}")
                d_act = self._b64_url(f"act/{row['id']}")
                d_det = self._b64_url(f"det/{row['id']}")

                html += f"""
                <tr>
                    <td>{row['placa']}</td>
                    <td>{row['marca']}</td>
                    <td>{row['color']}</td>
                    <td>{row['anio']}</td>
                    <td>{row['avaluo']}</td>
                    <td><a href="{base_path()}/?d={d_del}">Borrar</a></td>
                    <td><a href="{base_path()}/?d={d_act}">Actualizar</a></td>
                    <td><a href="{base_path()}/?d={d_det}">Detalle</a></td>
                </tr>
                """
        else:
            html += self._message_BD_Vacia("Tabla Vehiculo<br>")

        html += "</table>"
        return html

    # =========================================================
    # DETALLE
    # =========================================================
    def get_detail_vehiculo(self, id):

        sql = f"""
        SELECT v.placa, m.descripcion AS marca, v.motor, v.chasis,
               v.combustible, v.anio, c.descripcion AS color,
               v.foto, v.avaluo
        FROM vehiculo v, color c, marca m
        WHERE v.id={id} AND v.marca=m.id AND v.color=c.id;
        """

        cursor = self.con.cursor(dictionary=True)
        cursor.execute(sql)
        row = cursor.fetchone()

        if row is None:
            mensaje = f"desplegar el detalle del vehiculo con id= {id} <br>"
            return self._message_error(mensaje)

        html = f"""
        <table border="1" align="center">
            <tr><th colspan="2">DATOS DEL VEHÍCULO</th></tr>

            <tr><td>Placa:</td><td>{row['placa']}</td></tr>
            <tr><td>Marca:</td><td>{row['marca']}</td></tr>
            <tr><td>Motor:</td><td>{row['motor']}</td></tr>
            <tr><td>Chasis:</td><td>{row['chasis']}</td></tr>
            <tr><td>Combustible:</td><td>{row['combustible']}</td></tr>
            <tr><td>Anio:</td><td>{row['anio']}</td></tr>
            <tr><td>Color:</td><td>{row['color']}</td></tr>
            <tr><td>Avalúo:</td><th>${row['avaluo']} USD</th></tr>
            <tr><td>Valor Matrícula:</td>
                <th>${self._calculo_matricula(row['avaluo'])} USD</th>
            </tr>
            <tr>
                <th colspan="2">
                    <img src="{base_path()}/images/{row['foto']}" width="300px">
                </th>
            </tr>
            <tr>
                <th colspan="2">
                    <a href="{base_path()}/">Regresar</a>
                </th>
            </tr>
        </table>
        """
        return html

    # =========================================================
    # DELETE (IGUAL QUE TU PHP: SOLO MENSAJE)
    # =========================================================
    def delete_vehiculo(self, id):
        mensaje = f"PROXIMAMENTE SE ELIMINARA el vehiculo con id= {id} <br>"
        return self._message_error(mensaje)

    # =========================================================
    # MÉTODOS PRIVADOS (IGUAL QUE PHP)
    # =========================================================
    def _get_combo_db(self, tabla, valor, etiqueta, nombre, defecto=None):
        html = f'<select name="{nombre}">'
        cursor = self.con.cursor(dictionary=True)
        cursor.execute(f"SELECT {valor},{etiqueta} FROM {tabla};")
        rows = cursor.fetchall()

        for row in rows:
            selected = 'selected' if defecto == row[valor] else ''
            html += f'<option value="{row[valor]}" {selected}>{row[etiqueta]}</option>\n'
        html += '</select>'
        return html

    def _get_combo_anio(self, nombre, anio_inicial, defecto=None):
        html = f'<select name="{nombre}">'
        anio_actual = datetime.now().year
        for i in range(anio_inicial, anio_actual + 1):
            selected = 'selected' if defecto == i else ''
            html += f'<option value="{i}" {selected}>{i}</option>\n'
        html += '</select>'
        return html

    def _get_radio(self, arreglo, nombre, defecto=None):
        html = '<table border="0" align="left">'
        for etiqueta in arreglo:
            checked = "checked" if defecto == etiqueta else ""
            html += f"""
            <tr>
                <td>{etiqueta}</td>
                <td><input type="radio" value="{etiqueta}" name="{nombre}" {checked}/></td>
            </tr>
            """
        html += '</table>'
        return html

    def _calculo_matricula(self, avaluo):
        return f"{(float(avaluo) * 0.10):.2f}"

    def _message_error(self, tipo):
        return f"""
        <table border="0" align="center">
            <tr>
                <th>Error al {tipo} Favor contactar a .................... </th>
            </tr>
            <tr>
                <th><a href="{base_path()}/">Regresar</a></th>
            </tr>
        </table>
        """

    def _message_BD_Vacia(self, tipo):
        return f"""
        <table border="0" align="center">
            <tr>
                <th> NO existen registros en la {tipo} Favor contactar a .................... </th>
            </tr>
        </table>
        """

    def _message_ok(self, tipo):
        return f"""
        <table border="0" align="center">
            <tr>
                <th>El registro se {tipo} correctamente</th>
            </tr>
            <tr>
                <th><a href="{base_path()}/">Regresar</a></th>
            </tr>
        </table>
        """
