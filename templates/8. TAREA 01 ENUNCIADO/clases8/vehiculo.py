from flask import request
import base64
import os
import random
from datetime import datetime


class Vehiculo:

    def __init__(self, cn):
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
        self.con = cn

    # ======================= UPDATE =======================
    def update_vehiculo(self):

        self.id = request.form['id']
        self.placa = request.form['placa']
        self.motor = request.form['motor']
        self.chasis = request.form['chasis']

        self.marca = request.form['marcaCMB']
        self.anio = request.form['anio']
        self.color = request.form['colorCMB']
        self.combustible = request.form['combustibleRBT']

        sql = f"""
        UPDATE vehiculo SET
            placa='{self.placa}',
            marca={self.marca},
            motor='{self.motor}',
            chasis='{self.chasis}',
            combustible='{self.combustible}',
            anio='{self.anio}',
            color={self.color}
        WHERE id={self.id};
        """

        cursor = self.con.cursor()
        try:
            cursor.execute(sql)
            self.con.commit()
            return self._message_ok("MODIFICÓ")
        except Exception as e:
            return self._message_error("al modificar<br><br>" + str(e))

    # ======================= SAVE =======================
    def save_vehiculo(self):

        self.placa = request.form['placa']
        self.motor = request.form['motor']
        self.chasis = request.form['chasis']
        self.avaluo = request.form['avaluo']

        self.marca = request.form['marcaCMB']
        self.anio = request.form['anio']
        self.color = request.form['colorCMB']
        self.combustible = request.form['combustibleRBT']

        file = request.files.get('foto')
        if not file or file.filename == "":
            return self._message_error("Cargar la imagen")

        self.foto = file.filename

        os.makedirs("static/images", exist_ok=True)
        path = os.path.join("static/images", self.foto)

        try:
            file.save(path)
        except Exception as e:
            return self._message_error("Cargar la imagen<br><br>" + str(e))

        sql = f"""
        INSERT INTO vehiculo VALUES(
            NULL,
            '{self.placa}',
            {self.marca},
            '{self.motor}',
            '{self.chasis}',
            '{self.combustible}',
            '{self.anio}',
            {self.color},
            '{self.foto}',
            {self.avaluo}
        );
        """

        cursor = self.con.cursor()
        try:
            cursor.execute(sql)
            self.con.commit()
            return self._message_ok("GUARDÓ")
        except Exception as e:
            return self._message_error("guardar<br><br>" + str(e))

    # ======================= NOMBRE ARCHIVO =======================
    def _get_name_file(self, nombre_original, tamanio):

        tmp = nombre_original.split(".")
        ext = tmp[-1]
        cadena = ""

        while len(cadena) < tamanio:
            c = random.randint(65, 122)
            if 91 <= c <= 96:
                continue
            cadena += chr(c)

        return cadena + "." + ext

    # ======================= COMBOS =======================
    def _get_combo_db(self, tabla, valor, etiqueta, nombre, defecto):

        html = f'<select class="form-select" name="{nombre}">'
        cursor = self.con.cursor(dictionary=True)
        cursor.execute(f"SELECT {valor}, {etiqueta} FROM {tabla};")

        for row in cursor.fetchall():
            selected = "selected" if str(defecto) == str(row[valor]) else ""
            html += f'<option value="{row[valor]}" {selected}>{row[etiqueta]}</option>\n'

        return html + '</select>'

    def _get_combo_anio(self, nombre, anio_inicial, defecto):

        anio_actual = datetime.now().year
        html = f'<select class="form-select" name="{nombre}">'

        for i in range(anio_inicial, anio_actual + 1):
            selected = "selected" if str(i) == str(defecto) else ""
            html += f'<option value="{i}" {selected}>{i}</option>\n'

        return html + '</select>'

    def _get_radio(self, arreglo, nombre, defecto):

        html = '<div class="d-flex flex-wrap gap-3">'
        ya_seleccionado = False

        for etiqueta in arreglo:
            checked = ""
            if defecto is None and not ya_seleccionado:
                checked = "checked"
                ya_seleccionado = True
            elif defecto == etiqueta:
                checked = "checked"

            html += f'''
            <div class="form-check">
                <input class="form-check-input" type="radio" value="{etiqueta}" name="{nombre}" {checked}>
                <label class="form-check-label">{etiqueta}</label>
            </div>
            '''

        return html + '</div>'

    # ======================= FORM =======================
    def get_form(self, id=None):

        if id is None:
            self.placa = ""
            self.marca = ""
            self.motor = ""
            self.chasis = ""
            self.combustible = ""
            self.anio = ""
            self.color = ""
            self.foto = ""
            self.avaluo = ""

            flag = ""
            op = "new"
        else:
            sql = f"SELECT * FROM vehiculo WHERE id={id};"
            cursor = self.con.cursor(dictionary=True)
            cursor.execute(sql)
            row = cursor.fetchone()

            if not row:
                return self._message_error(f"tratar de actualizar el vehiculo con id= {id}")

            self.placa = row['placa']
            self.marca = row['marca']
            self.motor = row['motor']
            self.chasis = row['chasis']
            self.combustible = row['combustible']
            self.anio = row['anio']
            self.color = row['color']
            self.foto = row['foto']
            self.avaluo = row['avaluo']

            flag = "disabled"
            op = "update"

        combustibles = ["Gasolina", "Diesel", "Eléctrico"]

        html = f'''
        <div class="card shadow-sm">
            <div class="card-header bg-dark text-white fw-bold">DATOS VEHÍCULO</div>
            <div class="card-body">
                <form method="POST" action="app.py?mod=vehiculo" enctype="multipart/form-data">

                    <input type="hidden" name="id" value="{id}">
                    <input type="hidden" name="op" value="{op}">

                    <div class="row g-3">

                        <div class="col-md-4">
                            <label class="form-label fw-semibold">Placa</label>
                            <input class="form-control" type="text" name="placa" value="{self.placa}" required>
                        </div>

                        <div class="col-md-4">
                            <label class="form-label fw-semibold">Marca</label>
                            {self._get_combo_db("marca","id","descripcion","marcaCMB",self.marca)}
                        </div>

                        <div class="col-md-4">
                            <label class="form-label fw-semibold">Año</label>
                            {self._get_combo_anio("anio",1980,self.anio)}
                        </div>

                        <div class="col-md-6">
                            <label class="form-label fw-semibold">Motor</label>
                            <input class="form-control" type="text" name="motor" value="{self.motor}" required>
                        </div>

                        <div class="col-md-6">
                            <label class="form-label fw-semibold">Chasis</label>
                            <input class="form-control" type="text" name="chasis" value="{self.chasis}" required>
                        </div>

                        <div class="col-md-6">
                            <label class="form-label fw-semibold d-block">Combustible</label>
                            {self._get_radio(combustibles,"combustibleRBT",self.combustible)}
                        </div>

                        <div class="col-md-6">
                            <label class="form-label fw-semibold">Color</label>
                            {self._get_combo_db("color","id","descripcion","colorCMB",self.color)}
                        </div>

                        <div class="col-md-6">
                            <label class="form-label fw-semibold">Foto</label>
                            <input class="form-control" type="file" name="foto" {flag}>
                        </div>

                        <div class="col-md-6">
                            <label class="form-label fw-semibold">Avalúo</label>
                            <input class="form-control" type="text" name="avaluo" value="{self.avaluo}" {flag} required>
                        </div>

                    </div>

                    <hr class="my-4">

                    <div class="d-flex justify-content-center gap-2">
                        <button class="btn btn-success px-4" type="submit">GUARDAR</button>
                        <a class="btn btn-secondary px-4" href="app.py?mod=vehiculo">REGRESAR</a>
                    </div>

                </form>
            </div>
        </div>
        '''

        return html

    # ======================= LIST =======================
    def get_list(self):

        d_new = base64.b64encode(b"new/0").decode()

        html = f'''
        <div class="card shadow-sm">
            <div class="card-header d-flex justify-content-between align-items-center bg-dark text-white">
                <span class="fw-bold">LISTA DE VEHÍCULOS</span>
                <a class="btn btn-success btn-sm" href="app.py?mod=vehiculo&d={d_new}">+ NUEVO</a>
            </div>

            <div class="card-body">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Placa</th>
                            <th>Marca</th>
                            <th>Color</th>
                            <th>Año</th>
                            <th>Avalúo</th>
                            <th colspan="3">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
        '''

        sql = """
        SELECT v.id, v.placa, m.descripcion as marca, c.descripcion as color, v.anio, v.avaluo
        FROM vehiculo v, color c, marca m
        WHERE v.marca=m.id AND v.color=c.id;
        """

        cursor = self.con.cursor(dictionary=True)
        cursor.execute(sql)

        for row in cursor.fetchall():
            d_del = base64.b64encode(f"del/{row['id']}".encode()).decode()
            d_act = base64.b64encode(f"act/{row['id']}".encode()).decode()
            d_det = base64.b64encode(f"det/{row['id']}".encode()).decode()

            html += f'''
            <tr>
                <td>{row['placa']}</td>
                <td>{row['marca']}</td>
                <td>{row['color']}</td>
                <td>{row['anio']}</td>
                <td>$ {row['avaluo']}</td>
                <td><a href="app.py?mod=vehiculo&d={d_del}">Borrar</a></td>
                <td><a href="app.py?mod=vehiculo&d={d_act}">Actualizar</a></td>
                <td><a href="app.py?mod=vehiculo&d={d_det}">Detalle</a></td>
            </tr>
            '''

        html += '''
                    </tbody>
                </table>
            </div>
        </div>
        '''

        return html

    # ======================= DETAIL =======================
    def get_detail_vehiculo(self, id):

        sql = f"""
        SELECT v.placa, m.descripcion as marca, v.motor, v.chasis, v.combustible, v.anio,
               c.descripcion as color, v.foto, v.avaluo
        FROM vehiculo v, color c, marca m
        WHERE v.id={id} AND v.marca=m.id AND v.color=c.id;
        """

        cursor = self.con.cursor(dictionary=True)
        cursor.execute(sql)
        row = cursor.fetchone()

        if not row:
            return self._message_error(f"tratar de ver detalle del vehiculo con id= {id}")

        html = f'''
        <div class="card shadow-sm">
            <div class="card-header bg-dark text-white fw-bold">DATOS DEL VEHÍCULO</div>
            <div class="card-body">
                <div class="row g-3">
                    <div class="col-md-6"><b>Placa:</b> {row['placa']}</div>
                    <div class="col-md-6"><b>Marca:</b> {row['marca']}</div>
                    <div class="col-md-6"><b>Motor:</b> {row['motor']}</div>
                    <div class="col-md-6"><b>Chasis:</b> {row['chasis']}</div>
                    <div class="col-md-6"><b>Combustible:</b> {row['combustible']}</div>
                    <div class="col-md-6"><b>Año:</b> {row['anio']}</div>
                    <div class="col-md-6"><b>Color:</b> {row['color']}</div>
                    <div class="col-md-6"><b>Avalúo:</b> $ {row['avaluo']} USD</div>
                    <div class="col-md-12"><b>Valor Matrícula:</b> $ {self._calculo_matricula(row['avaluo'])} USD</div>
                </div>

                <hr class="my-4">

                <div class="text-center">
                    <img class="img-fluid rounded border" src="static/images/{row['foto']}" style="max-width:300px;">
                </div>

                <hr class="my-4">

                <div class="text-center">
                    <a class="btn btn-secondary px-4" href="app.py?mod=vehiculo">REGRESAR</a>
                </div>
            </div>
        </div>
        '''

        return html

    # ======================= DELETE =======================
    def delete_vehiculo(self, id):

        sql = f"DELETE FROM vehiculo WHERE id={id};"
        cursor = self.con.cursor()

        try:
            cursor.execute(sql)
            self.con.commit()
            return self._message_ok("ELIMINÓ")
        except Exception as e:
            return self._message_error("eliminar<br><br>" + str(e))

    # ======================= CALCULO =======================
    def _calculo_matricula(self, avaluo):
        return f"{float(avaluo) * 0.10:.2f}"

    # ======================= MENSAJES =======================
    def _message_error(self, tipo):

        return f'''
        <div class="alert alert-danger shadow-sm">
            <div class="fw-bold mb-1">Error al {tipo}.</div>
            <div>Favor contactar a ....................</div>
            <hr>
            <a class="btn btn-outline-danger btn-sm" href="app.py?mod=vehiculo">Regresar</a>
        </div>
        '''

    def _message_ok(self, tipo):

        return f'''
        <div class="alert alert-success shadow-sm">
            <div class="fw-bold mb-1">El registro se {tipo} correctamente</div>
            <hr>
            <a class="btn btn-outline-success btn-sm" href="app.py?mod=vehiculo">Regresar</a>
        </div>
        '''
