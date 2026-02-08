from flask import request
import base64
import os


class Marca:
    def __init__(self, cn):
        self.id = None
        self.descripcion = None
        self.pais = None
        self.direccion = None
        self.foto = None
        self.con = cn

    # ========================= GUARDAR =========================
    def save_marca(self):
        self.descripcion = request.form['descripcion']
        self.pais = request.form['pais']
        self.direccion = request.form['direccion']

        file = request.files.get('foto')
        if not file or file.filename == "":
            return self._message_error("cargar la imagen")

        self.foto = file.filename

        # Asegura que exista la carpeta
        os.makedirs("static/images", exist_ok=True)
        path = os.path.join("static/images", self.foto)

        try:
            file.save(path)
        except Exception as e:
            return self._message_error("cargar la imagen<br><br>" + str(e))

        sql = f"""
        INSERT INTO marca VALUES(
            NULL,
            '{self.descripcion}',
            '{self.pais}',
            '{self.direccion}',
            '{self.foto}'
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
    def update_marca(self):
        self.id = int(request.form['id'])
        self.descripcion = request.form['descripcion']
        self.pais = request.form['pais']
        self.direccion = request.form['direccion']

        file = request.files.get('foto')
        foto_nueva = file.filename if file else ""

        if foto_nueva != "":
            self.foto = foto_nueva
            os.makedirs("static/images", exist_ok=True)
            path = os.path.join("static/images", self.foto)

            try:
                file.save(path)
            except Exception as e:
                return self._message_error("cargar la imagen<br><br>" + str(e))

            sql = f"""
            UPDATE marca SET
                descripcion='{self.descripcion}',
                pais='{self.pais}',
                direccion='{self.direccion}',
                foto='{self.foto}'
            WHERE id={self.id};
            """
        else:
            sql = f"""
            UPDATE marca SET
                descripcion='{self.descripcion}',
                pais='{self.pais}',
                direccion='{self.direccion}'
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
            self.descripcion = ""
            self.pais = ""
            self.direccion = ""
            self.foto = ""
            op = "new"
        else:
            id = int(id)
            sql = f"SELECT * FROM marca WHERE id={id};"
            cursor = self.con.cursor(dictionary=True)
            cursor.execute(sql)
            row = cursor.fetchone()

            if not row:
                return self._message_error("consultar marca")

            self.descripcion = row['descripcion']
            self.pais = row['pais']
            self.direccion = row['direccion']
            self.foto = row['foto']
            op = "update"

        html = f'''
        <div class="card shadow-sm">
            <div class="card-header bg-dark text-white fw-bold">DATOS MARCA</div>
            <div class="card-body">
                <form method="POST" action="app.py?mod=marca" enctype="multipart/form-data">
                    <input type="hidden" name="id" value="{'' if id is None else int(id)}">
                    <input type="hidden" name="op" value="{op}">

                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label fw-semibold">Descripción</label>
                            <input class="form-control" type="text" name="descripcion" value="{self.descripcion}" required>
                        </div>

                        <div class="col-md-6">
                            <label class="form-label fw-semibold">País</label>
                            <input class="form-control" type="text" name="pais" value="{self.pais}" required>
                        </div>

                        <div class="col-12">
                            <label class="form-label fw-semibold">Dirección</label>
                            <input class="form-control" type="text" name="direccion" value="{self.direccion}" required>
                        </div>

                        <div class="col-12">
                            <label class="form-label fw-semibold">Foto</label>
                            <input class="form-control" type="file" name="foto">
                            <div class="form-text">En actualizar, la foto es opcional.</div>
                        </div>
                    </div>

                    <hr class="my-4">

                    <div class="d-flex justify-content-center gap-2">
                        <button class="btn btn-success px-4" type="submit">GUARDAR</button>
                        <a class="btn btn-secondary px-4" href="app.py?mod=marca">REGRESAR</a>
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
                <span class="fw-bold">LISTA DE MARCAS</span>
                <a class="btn btn-success btn-sm" href="app.py?mod=marca&d={d_new}">+ NUEVO</a>
            </div>

            <div class="card-body">
                <table class="table table-striped table-hover align-middle">
                    <thead class="table-secondary">
                        <tr>
                            <th>Descripción</th>
                            <th>País</th>
                            <th>Dirección</th>
                            <th>Foto</th>
                            <th class="text-center" colspan="3">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
        '''

        cursor = self.con.cursor(dictionary=True)
        cursor.execute("SELECT id, descripcion, pais, direccion, foto FROM marca;")
        rows = cursor.fetchall()

        if not rows:
            html += '<tr><td colspan="7" class="text-center fw-semibold">NO existen registros</td></tr>'
        else:
            for row in rows:
                d_del = base64.b64encode(f"del/{row['id']}".encode()).decode()
                d_act = base64.b64encode(f"act/{row['id']}".encode()).decode()
                d_det = base64.b64encode(f"det/{row['id']}".encode()).decode()

                html += f'''
                <tr>
                    <td>{row['descripcion']}</td>
                    <td>{row['pais']}</td>
                    <td>{row['direccion']}</td>
                    <td>{row['foto']}</td>
                    <td class="text-center"><a class="btn btn-outline-danger btn-sm" href="app.py?mod=marca&d={d_del}">Borrar</a></td>
                    <td class="text-center"><a class="btn btn-outline-primary btn-sm" href="app.py?mod=marca&d={d_act}">Actualizar</a></td>
                    <td class="text-center"><a class="btn btn-outline-dark btn-sm" href="app.py?mod=marca&d={d_det}">Detalle</a></td>
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
    def get_detail_marca(self, id):
        id = int(id)
        sql = f"SELECT descripcion, pais, direccion, foto FROM marca WHERE id={id};"
        cursor = self.con.cursor(dictionary=True)
        cursor.execute(sql)
        row = cursor.fetchone()

        if not row:
            return self._message_error("detalle")

        foto_src = f"static/images/{row['foto']}"

        html = f'''
        <div class="card shadow-sm">
            <div class="card-header bg-dark text-white fw-bold">DETALLE MARCA</div>
            <div class="card-body">
                <div class="row g-3">
                    <div class="col-md-6"><span class="fw-semibold">Descripción:</span> {row['descripcion']}</div>
                    <div class="col-md-6"><span class="fw-semibold">País:</span> {row['pais']}</div>
                    <div class="col-12"><span class="fw-semibold">Dirección:</span> {row['direccion']}</div>
                </div>

                <hr class="my-4">

                <div class="text-center">
                    <img class="img-fluid rounded border" src="{foto_src}" style="max-width:300px">
                </div>

                <hr class="my-4">

                <div class="text-center">
                    <a class="btn btn-secondary px-4" href="app.py?mod=marca">REGRESAR</a>
                </div>
            </div>
        </div>
        '''
        return html

    # ========================= BORRAR =========================
    def delete_marca(self, id):
        id = int(id)
        sql = f"DELETE FROM marca WHERE id={id};"
        cursor = self.con.cursor()

        try:
            cursor.execute(sql)
            self.con.commit()
            return self._message_ok("ELIMINÓ")
        except Exception as e:
            return self._message_error("eliminar<br><br>" + str(e))

    # ========================= MENSAJES =========================
    def _message_error(self, tipo):
        return f'''
        <div class="alert alert-danger shadow-sm" role="alert">
            <div class="fw-bold mb-1">Error al {tipo}</div>
            <hr>
            <a class="btn btn-outline-danger btn-sm" href="app.py?mod=marca">Regresar</a>
        </div>
        '''

    def _message_ok(self, tipo):
        return f'''
        <div class="alert alert-success shadow-sm" role="alert">
            <div class="fw-bold mb-1">El registro se {tipo} correctamente</div>
            <hr>
            <a class="btn btn-outline-success btn-sm" href="app.py?mod=marca">Regresar</a>
        </div>
        '''
