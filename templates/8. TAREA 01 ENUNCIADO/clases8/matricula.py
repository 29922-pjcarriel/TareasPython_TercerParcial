from flask import request
import base64
from datetime import datetime


class Matricula:

    def __init__(self, cn):
        self.id = None
        self.fecha = None
        self.vehiculo = None
        self.agencia = None
        self.anio = None
        self.con = cn

    # ========================= GUARDAR =========================
    def save_matricula(self):

        self.fecha = request.form['fecha']
        self.vehiculo = request.form['vehiculoCMB']
        self.agencia = request.form['agenciaCMB']
        self.anio = request.form['anio']

        sql = f"""
        INSERT INTO matricula VALUES(
            NULL,
            '{self.fecha}',
            {self.vehiculo},
            {self.agencia},
            {self.anio}
        );
        """

        cursor = self.con.cursor()
        try:
            cursor.execute(sql)
            self.con.commit()
            return self._message_ok("GUARDÓ")
        except Exception as e:
            return self._message_error("guardar<br><br>" + str(e))

    # ========================= ACTUALIZAR =========================
    def update_matricula(self):

        self.id = request.form['id']
        self.fecha = request.form['fecha']
        self.vehiculo = request.form['vehiculoCMB']
        self.agencia = request.form['agenciaCMB']
        self.anio = request.form['anio']

        sql = f"""
        UPDATE matricula SET
            fecha='{self.fecha}',
            vehiculo={self.vehiculo},
            agencia={self.agencia},
            anio={self.anio}
        WHERE id={self.id};
        """

        cursor = self.con.cursor()
        try:
            cursor.execute(sql)
            self.con.commit()
            return self._message_ok("MODIFICÓ")
        except Exception as e:
            return self._message_error("modificar<br><br>" + str(e))

    # ========================= FORMULARIO =========================
    def get_form(self, id=None):

        if id is None:
            self.fecha = ""
            self.vehiculo = ""
            self.agencia = ""
            self.anio = ""
            op = "new"
        else:
            sql = f"SELECT * FROM matricula WHERE id={id};"
            cursor = self.con.cursor(dictionary=True)
            cursor.execute(sql)
            row = cursor.fetchone()

            if not row:
                return self._message_error("consultar matrícula")

            self.fecha = row['fecha']
            self.vehiculo = row['vehiculo']
            self.agencia = row['agencia']
            self.anio = row['anio']
            op = "update"

        html = f'''
        <div class="card shadow-sm">
            <div class="card-header bg-dark text-white fw-bold">DATOS MATRÍCULA</div>
            <div class="card-body">
                <form method="POST" action="app.py?mod=matricula">
                    <input type="hidden" name="id" value="{id}">
                    <input type="hidden" name="op" value="{op}">

                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label fw-semibold">Fecha</label>
                            <input class="form-control" type="date" name="fecha" value="{self.fecha}" required>
                        </div>

                        <div class="col-md-6">
                            <label class="form-label fw-semibold">Año</label>
                            {self._get_combo_anio("anio", 2000, self.anio)}
                        </div>

                        <div class="col-md-6">
                            <label class="form-label fw-semibold">Vehículo</label>
                            {self._get_combo_db("vehiculo", "id", "placa", "vehiculoCMB", self.vehiculo)}
                        </div>

                        <div class="col-md-6">
                            <label class="form-label fw-semibold">Agencia</label>
                            {self._get_combo_db("agencia", "id", "descripcion", "agenciaCMB", self.agencia)}
                        </div>
                    </div>

                    <hr class="my-4">

                    <div class="d-flex justify-content-center gap-2">
                        <button class="btn btn-success px-4" type="submit">GUARDAR</button>
                        <a class="btn btn-secondary px-4" href="app.py?mod=matricula">REGRESAR</a>
                    </div>

                </form>
            </div>
        </div>
        '''

        return html

    # ========================= LISTA =========================
    def get_list(self):

        d_new = base64.b64encode(b"new/0").decode()

        html = f'''
        <div class="card shadow-sm">
            <div class="card-header d-flex justify-content-between align-items-center bg-dark text-white">
                <span class="fw-bold">LISTA DE MATRÍCULAS</span>
                <a class="btn btn-success btn-sm" href="app.py?mod=matricula&d={d_new}">+ NUEVO</a>
            </div>

            <div class="card-body">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Fecha</th>
                            <th>Vehículo</th>
                            <th>Agencia</th>
                            <th>Año</th>
                            <th colspan="3">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
        '''

        sql = """
        SELECT m.id, m.fecha, v.placa AS vehiculo, a.descripcion AS agencia, m.anio
        FROM matricula m, vehiculo v, agencia a
        WHERE m.vehiculo=v.id AND m.agencia=a.id;
        """

        cursor = self.con.cursor(dictionary=True)
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            d_del = base64.b64encode(f"del/{row['id']}".encode()).decode()
            d_act = base64.b64encode(f"act/{row['id']}".encode()).decode()
            d_det = base64.b64encode(f"det/{row['id']}".encode()).decode()

            html += f'''
            <tr>
                <td>{row['fecha']}</td>
                <td>{row['vehiculo']}</td>
                <td>{row['agencia']}</td>
                <td>{row['anio']}</td>
                <td><a href="app.py?mod=matricula&d={d_del}">Borrar</a></td>
                <td><a href="app.py?mod=matricula&d={d_act}">Actualizar</a></td>
                <td><a href="app.py?mod=matricula&d={d_det}">Detalle</a></td>
            </tr>
            '''

        html += '''
                    </tbody>
                </table>
            </div>
        </div>
        '''

        return html

    # ========================= DETALLE =========================
    def get_detail_matricula(self, id):

        sql = f"""
        SELECT m.fecha, v.placa AS vehiculo, a.descripcion AS agencia, m.anio
        FROM matricula m, vehiculo v, agencia a
        WHERE m.id={id} AND m.vehiculo=v.id AND m.agencia=a.id;
        """

        cursor = self.con.cursor(dictionary=True)
        cursor.execute(sql)
        row = cursor.fetchone()

        if not row:
            return self._message_error("detalle")

        html = f'''
        <div class="card shadow-sm">
            <div class="card-header bg-dark text-white fw-bold">DETALLE MATRÍCULA</div>
            <div class="card-body">
                <div class="row g-3">
                    <div class="col-md-6"><b>Fecha:</b> {row['fecha']}</div>
                    <div class="col-md-6"><b>Vehículo:</b> {row['vehiculo']}</div>
                    <div class="col-md-6"><b>Agencia:</b> {row['agencia']}</div>
                    <div class="col-md-6"><b>Año:</b> {row['anio']}</div>
                </div>

                <hr class="my-4">

                <div class="text-center">
                    <a class="btn btn-secondary px-4" href="app.py?mod=matricula">REGRESAR</a>
                </div>
            </div>
        </div>
        '''

        return html

    # ========================= BORRAR =========================
    def delete_matricula(self, id):

        sql = f"DELETE FROM matricula WHERE id={id};"
        cursor = self.con.cursor()

        try:
            cursor.execute(sql)
            self.con.commit()
            return self._message_ok("ELIMINÓ")
        except:
            return self._message_error("eliminar")

    # ========================= UTILIDADES =========================
    def _get_combo_db(self, tabla, valor, etiqueta, nombre, defecto):

        html = f'<select class="form-select" name="{nombre}">'
        cursor = self.con.cursor(dictionary=True)
        cursor.execute(f"SELECT {valor}, {etiqueta} FROM {tabla};")

        for row in cursor.fetchall():
            selected = "selected" if str(defecto) == str(row[valor]) else ""
            html += f'<option value="{row[valor]}" {selected}>{row[etiqueta]}</option>'

        return html + '</select>'

    def _get_combo_anio(self, nombre, inicio, defecto):

        actual = datetime.now().year
        html = f'<select class="form-select" name="{nombre}">'

        for i in range(inicio, actual + 1):
            selected = "selected" if str(i) == str(defecto) else ""
            html += f'<option value="{i}" {selected}>{i}</option>'

        return html + '</select>'

    # ========================= MENSAJES =========================
    def _message_error(self, t):

        return f'''
        <div class="alert alert-danger shadow-sm">
            <div class="fw-bold mb-1">Error al {t}</div>
            <hr>
            <a class="btn btn-outline-danger btn-sm" href="app.py?mod=matricula">Regresar</a>
        </div>
        '''

    def _message_ok(self, t):

        return f'''
        <div class="alert alert-success shadow-sm">
            <div class="fw-bold mb-1">Se {t} correctamente</div>
            <hr>
            <a class="btn btn-outline-success btn-sm" href="app.py?mod=matricula">Regresar</a>
        </div>
        '''
