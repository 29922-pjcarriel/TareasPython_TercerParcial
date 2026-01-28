# routes/class_matricula.py
# CRUD MATRÍCULA – CORREGIDO
# FK AGENCIA + FK VEHICULO CORRECTOS

import base64
from datetime import datetime
from urllib.parse import quote_plus


class Matricula:

    # =====================================================
    # CONSTRUCTOR
    # =====================================================
    def __init__(self, cn):
        self.con = cn
        print("EJECUTANDOSE EL CONSTRUCTOR MATRICULA<br><br>")

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
                "fecha": "",
                "vehiculo": "",
                "agencia": "",
                "anio": ""
            }
            op = "new"
            titulo = "Nueva Matrícula"
        else:
            cur = self.con.cursor(dictionary=True)
            cur.execute("SELECT * FROM matricula WHERE id=%s", (id,))
            row = cur.fetchone()

            if row is None:
                return self._message_error(
                    f"tratar de actualizar la matrícula con id= {id}<br>"
                )

            op = "update"
            titulo = "Actualizar Matrícula"

        html = f"""
        <div class="container py-4">
            <div class="card shadow-lg">
                <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
                    <div>
                        <h4 class="mb-0">{titulo}</h4>
                        <small class="opacity-75">Formulario de registro</small>
                    </div>
                    <a href="?mod=matricula" class="btn btn-light">Regresar</a>
                </div>

                <div class="card-body">
                    <form method="POST" action="?mod=matricula">

                        <input type="hidden" name="id" value="{id or 0}">
                        <input type="hidden" name="op" value="{op}">

                        <div class="row g-3">

                            <div class="col-md-4">
                                <label class="form-label fw-semibold">Fecha</label>
                                <input type="date" class="form-control"
                                       name="fecha" value="{row['fecha']}" required>
                            </div>

                            <div class="col-md-4">
                                <label class="form-label fw-semibold">Vehículo</label>
                                {self._get_combo_vehiculo_bs("vehiculo", row["vehiculo"])}
                            </div>

                            <div class="col-md-4">
                                <label class="form-label fw-semibold">Agencia</label>
                                {self._get_combo_agencia_bs("agencia", row["agencia"])}
                            </div>

                            <div class="col-md-4">
                                <label class="form-label fw-semibold">Año</label>
                                {self._get_combo_anio_bs("anio", 2000, row["anio"])}
                            </div>

                        </div>

                        <div class="mt-4 text-end">
                            <input type="submit" class="btn btn-success px-4"
                                   name="Guardar" value="GUARDAR">
                            <a href="?mod=matricula" class="btn btn-secondary ms-2">Cancelar</a>
                        </div>

                    </form>
                </div>
            </div>
        </div>
        """

        return html

    # =====================================================
    # GUARDAR (INSERT / UPDATE)
    # =====================================================
    def save_matricula(self, data):

        cur = self.con.cursor()

        if data["op"] == "new":
            cur.execute("""
                INSERT INTO matricula (fecha, vehiculo, agencia, anio)
                VALUES (%s,%s,%s,%s)
            """, (
                data["fecha"],
                data["vehiculo"],
                data["agencia"],
                data["anio"]
            ))
            self.con.commit()
            return self._message_ok("insertó")

        if data["op"] == "update":
            cur.execute("""
                UPDATE matricula SET
                    fecha=%s,
                    vehiculo=%s,
                    agencia=%s,
                    anio=%s
                WHERE id=%s
            """, (
                data["fecha"],
                data["vehiculo"],
                data["agencia"],
                data["anio"],
                data["id"]
            ))
            self.con.commit()
            return self._message_ok("actualizó")

        return self._message_error("guardar")

    # =====================================================
    # LISTA
    # =====================================================
    def get_list(self):

        html = """
        <div class="container py-4">
            <div class="card shadow-lg">
                <div class="card-header bg-success text-white d-flex justify-content-between">
                    <h4 class="mb-0">Lista de Matrículas</h4>
                    <a href="?mod=matricula&d={}" class="btn btn-light">Nueva</a>
                </div>
                <div class="card-body p-0">
                    <table class="table table-striped table-hover text-center mb-0">
                        <thead class="table-dark">
                            <tr>
                                <th>Fecha</th>
                                <th>Vehículo</th>
                                <th>Agencia</th>
                                <th>Año</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
        """.format(self._b64("new/0"))

        cur = self.con.cursor(dictionary=True)
        cur.execute("""
            SELECT m.id,
                   m.fecha,
                   v.placa AS vehiculo,
                   a.descripcion AS agencia,
                   m.anio
            FROM matricula m
            JOIN vehiculo v ON m.vehiculo = v.id
            JOIN agencia a ON m.agencia = a.id
        """)

        for r in cur.fetchall():
            html += f"""
            <tr>
                <td>{r['fecha']}</td>
                <td>{r['vehiculo']}</td>
                <td>{r['agencia']}</td>
                <td>{r['anio']}</td>
                <td>
                    <a class="btn btn-sm btn-info"
                       href="?mod=matricula&d={self._b64(f'det/{r["id"]}')}">Detalle</a>
                    <a class="btn btn-sm btn-warning"
                       href="?mod=matricula&d={self._b64(f'act/{r["id"]}')}">Editar</a>
                    <a class="btn btn-sm btn-danger"
                       href="?mod=matricula&d={self._b64(f'del/{r["id"]}')}">Borrar</a>
                </td>
            </tr>
            """

        html += """
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        """

        return html

    # =====================================================
    # DETALLE
    # =====================================================
    def get_detail_matricula(self, id):

        cur = self.con.cursor(dictionary=True)
        cur.execute("""
            SELECT m.fecha,
                   v.placa AS vehiculo,
                   a.descripcion AS agencia,
                   m.anio
            FROM matricula m
            JOIN vehiculo v ON m.vehiculo = v.id
            JOIN agencia a ON m.agencia = a.id
            WHERE m.id=%s
        """, (id,))

        row = cur.fetchone()

        if row is None:
            return self._message_error("desplegar el detalle")

        return f"""
        <div class="container py-4">
            <div class="card shadow-lg">
                <div class="card-header bg-info text-white">Detalle Matrícula</div>
                <div class="card-body">
                    <table class="table table-bordered">
                        <tr><th>Fecha</th><td>{row['fecha']}</td></tr>
                        <tr><th>Vehículo</th><td>{row['vehiculo']}</td></tr>
                        <tr><th>Agencia</th><td>{row['agencia']}</td></tr>
                        <tr><th>Año</th><td>{row['anio']}</td></tr>
                    </table>
                </div>
            </div>
        </div>
        """

    # =====================================================
    # BORRAR
    # =====================================================
    def delete_matricula(self, id):
        cur = self.con.cursor()
        cur.execute("DELETE FROM matricula WHERE id=%s", (id,))
        self.con.commit()
        return self._message_ok("eliminó")

    # =====================================================
    # COMBOS
    # =====================================================
    def _get_combo_vehiculo_bs(self, nombre, defecto):
        html = f'<select class="form-select" name="{nombre}" required>'
        cur = self.con.cursor(dictionary=True)
        cur.execute("SELECT id, placa FROM vehiculo")
        for r in cur.fetchall():
            sel = "selected" if r["id"] == defecto else ""
            html += f'<option value="{r["id"]}" {sel}>{r["placa"]}</option>'
        html += "</select>"
        return html

    def _get_combo_agencia_bs(self, nombre, defecto):
        html = f'<select class="form-select" name="{nombre}" required>'
        cur = self.con.cursor(dictionary=True)
        cur.execute("SELECT id, descripcion FROM agencia")
        for r in cur.fetchall():
            sel = "selected" if r["id"] == defecto else ""
            html += f'<option value="{r["id"]}" {sel}>{r["descripcion"]}</option>'
        html += "</select>"
        return html

    def _get_combo_anio_bs(self, nombre, inicio, defecto):
        html = f'<select class="form-select" name="{nombre}">'
        actual = datetime.now().year
        defecto = int(defecto) if defecto else None
        for i in range(inicio, actual + 1):
            sel = "selected" if i == defecto else ""
            html += f'<option value="{i}" {sel}>{i}</option>'
        html += "</select>"
        return html

    # =====================================================
    # MENSAJES
    # =====================================================
    def _message_error(self, txt):
        return f"""
        <div class="container py-4">
            <div class="alert alert-danger text-center">
                Error al {txt}
            </div>
        </div>
        """

    def _message_ok(self, txt):
        return f"""
        <div class="container py-4">
            <div class="card shadow-sm">
                <div class="card-body text-center">
                    <div class="alert alert-success mb-4">
                        <i class="bi bi-check-circle-fill"></i>
                        El registro se {txt} correctamente
                    </div>

                    <a href="?mod=matricula"
                    class="btn btn-primary px-4">
                        <i class="bi bi-list"></i>
                        Regresar a la lista
                    </a>
                </div>
            </div>
        </div>
        """

