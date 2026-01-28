# routes/class_vehiculo.py
# CLON FUNCIONAL DEL class.vehiculo.php
# CRUD COMPLETO + BD REAL + FK CONTROLADA
# (MISMA LÓGICA, SOLO MEJOR DISEÑO CON BOOTSTRAP)

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
    # BOOTSTRAP BASE
    # =====================================================
    def _bootstrap_head(self, title="CRUD Vehículo"):
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>

            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">

            <style>
                body {{ background:#f4f6f9; }}
                .card {{ border-radius:14px; }}
                .table thead th {{ vertical-align: middle; }}
                .btn {{ border-radius:10px; }}
                .badge-money {{ font-size: .95rem; }}
            </style>
        </head>
        <body>
        """

    def _bootstrap_footer(self):
        return """
        </body>
        </html>
        """

    # =====================================================
    # BASE64 PARA ?d=
    # =====================================================
    def _b64(self, txt):
        return quote_plus(
            base64.b64encode(txt.encode("utf-8")).decode("utf-8")
        )

    # =====================================================
    # FORMULARIO (NEW / UPDATE)  ✅ FUNCIONAL CON app.py
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
            titulo = "Nuevo Vehículo"
            # en NEW permitimos subir foto y escribir avaluo
            flag_file = ""
            flag_avaluo = ""
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
            titulo = "Actualizar Vehículo"
            # En UPDATE normalmente dejas avaluo editable (si tú quieres bloquearlo, pon disabled)
            flag_file = ""      # permitir cambiar foto
            flag_avaluo = ""    # permitir cambiar avaluo

        combustibles = ["Gasolina", "Diesel", "Eléctrico"]

        html = f"""
        <div class="container py-4">
            <div class="card shadow-lg">
                <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                    <div>
                        <h4 class="mb-0"><i class="bi bi-car-front-fill"></i> {titulo}</h4>
                        <small class="opacity-75">Formulario de registro</small>
                    </div>
                    <a href="?" class="btn btn-light fw-semibold">
                        <i class="bi bi-arrow-left"></i> Regresar
                    </a>
                </div>

                <div class="card-body">
                    <form method="POST" action="?" enctype="multipart/form-data">

                        <input type="hidden" name="id" value="{id or 0}">
                        <input type="hidden" name="op" value="{op}">
                        <input type="hidden" name="foto_actual" value="{row['foto']}">

                        <div class="row g-3">
                            <div class="col-md-4">
                                <label class="form-label fw-semibold">Placa</label>
                                <input type="text" class="form-control" name="placa" value="{row['placa']}" required>
                            </div>

                            <div class="col-md-4">
                                <label class="form-label fw-semibold">Marca</label>
                                {self._get_combo_db_bs("marca","id","descripcion","marca",row["marca"])}
                            </div>

                            <div class="col-md-4">
                                <label class="form-label fw-semibold">Color</label>
                                {self._get_combo_db_bs("color","id","descripcion","color",row["color"])}
                            </div>

                            <div class="col-md-6">
                                <label class="form-label fw-semibold">Motor</label>
                                <input type="text" class="form-control" name="motor" value="{row['motor']}">
                            </div>

                            <div class="col-md-6">
                                <label class="form-label fw-semibold">Chasis</label>
                                <input type="text" class="form-control" name="chasis" value="{row['chasis']}">
                            </div>

                            <div class="col-md-6">
                                <label class="form-label fw-semibold d-block">Combustible</label>
                                {self._get_radio_bs(combustibles,"combustible",row["combustible"])}
                            </div>

                            <div class="col-md-6">
                                <label class="form-label fw-semibold">Año</label>
                                {self._get_combo_anio_bs("anio",1950,row["anio"])}
                            </div>

                            <div class="col-md-6">
                                <label class="form-label fw-semibold">Foto</label>
                                <input type="file" class="form-control" name="foto" {flag_file}>
                                <div class="form-text">
                                    Actual: <span class="text-muted">{row['foto'] or "Sin foto"}</span>
                                </div>
                            </div>

                            <div class="col-md-6">
                                <label class="form-label fw-semibold">Avalúo</label>
                                <input type="text" class="form-control" name="avaluo" value="{row['avaluo']}" {flag_avaluo} required>
                            </div>
                        </div>

                        <div class="mt-4 text-end">
                            <!-- ✅ CLAVE: name="Guardar" para que tu app.py detecte POST -->
                            <input type="submit" class="btn btn-success px-4"
                                   name="Guardar" value="GUARDAR">
                            <a href="?" class="btn btn-secondary ms-2">Cancelar</a>
                        </div>

                    </form>
                </div>
            </div>
        </div>
        """

        return self._bootstrap_head("Formulario Vehículo") + html + self._bootstrap_footer()

    # =====================================================
    # GUARDAR (INSERT / UPDATE) ✅ BD REAL
    # =====================================================
    def save_vehiculo(self, data, files):

        cur = self.con.cursor()
        foto_nombre = data.get("foto_actual", "")

        # subir foto si llega
        if files and "foto" in files and files["foto"].filename:
            foto = files["foto"]
            foto_nombre = foto.filename
            # guarda en carpeta images del proyecto
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

        return self._message_error("guardar")

    # =====================================================
    # LISTA (BOOTSTRAP BONITO) ✅ MISMA LÓGICA
    # =====================================================
    def get_list(self):

        html = f"""
        <div class="container py-4">
            <div class="card shadow-lg">
                <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                    <div>
                        <h4 class="mb-0"><i class="bi bi-car-front-fill"></i> Lista de Vehículos</h4>
                        <small class="opacity-75">Gestión de registros</small>
                    </div>
                    <a href="?d={self._b64('new/0')}" class="btn btn-light fw-semibold">
                        <i class="bi bi-plus-circle"></i> Nuevo
                    </a>
                </div>

                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-striped table-hover mb-0 align-middle text-center">
                            <thead class="table-dark">
                                <tr>
                                    <th>Placa</th>
                                    <th>Marca</th>
                                    <th>Color</th>
                                    <th>Año</th>
                                    <th>Avalúo</th>
                                    <th style="width:220px">Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
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
                <td class="fw-semibold">{r['placa']}</td>
                <td>{r['marca']}</td>
                <td>{r['color']}</td>
                <td>{r['anio']}</td>
                <td><span class="badge bg-success badge-money">${r['avaluo']}</span></td>
                <td>
                    <a class="btn btn-outline-info btn-sm me-1"
                       href="?d={self._b64(f'det/{r["id"]}')}">
                       <i class="bi bi-eye"></i> Detalle
                    </a>
                    <a class="btn btn-outline-warning btn-sm me-1"
                       href="?d={self._b64(f'act/{r["id"]}')}">
                       <i class="bi bi-pencil"></i> Editar
                    </a>
                    <a class="btn btn-outline-danger btn-sm"
                       href="?d={self._b64(f'del/{r["id"]}')}">
                       <i class="bi bi-trash"></i> Borrar
                    </a>
                </td>
            </tr>
            """

        html += """
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="card-footer text-center text-muted">
                    CRUD Vehículo – Flask + MySQL
                </div>
            </div>
        </div>
        """

        return self._bootstrap_head("Lista Vehículos") + html + self._bootstrap_footer()

    # =====================================================
    # DETALLE (CON MATRÍCULA + IMAGEN) ✅
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

        html = f"""
        <div class="container py-4">
            <div class="card shadow-lg">
                <div class="card-header bg-info text-white d-flex justify-content-between align-items-center">
                    <h4 class="mb-0"><i class="bi bi-info-circle"></i> Datos del Vehículo</h4>
                    <a href="?" class="btn btn-light fw-semibold">
                        <i class="bi bi-arrow-left"></i> Regresar
                    </a>
                </div>

                <div class="card-body">
                    <div class="row g-3 align-items-center">
                        <div class="col-md-5 text-center">
                            <img src="images/{row['foto']}" class="img-thumbnail" style="max-width:300px;">
                        </div>

                        <div class="col-md-7">
                            <table class="table table-bordered mb-0">
                                <tr><th>Placa</th><td>{row['placa']}</td></tr>
                                <tr><th>Marca</th><td>{row['marca']}</td></tr>
                                <tr><th>Motor</th><td>{row['motor']}</td></tr>
                                <tr><th>Chasis</th><td>{row['chasis']}</td></tr>
                                <tr><th>Combustible</th><td>{row['combustible']}</td></tr>
                                <tr><th>Año</th><td>{row['anio']}</td></tr>
                                <tr><th>Color</th><td>{row['color']}</td></tr>
                                <tr>
                                    <th>Avalúo</th>
                                    <td><span class="badge bg-success fs-6">${row['avaluo']} USD</span></td>
                                </tr>
                                <tr>
                                    <th>Valor Matrícula</th>
                                    <td><span class="badge bg-warning text-dark fs-6">
                                        ${self._calculo_matricula(row['avaluo'])} USD
                                    </span></td>
                                </tr>
                            </table>
                        </div>
                    </div>
                </div>

                <div class="card-footer text-center">
                    <a href="?" class="btn btn-secondary">
                        <i class="bi bi-arrow-left"></i> Regresar
                    </a>
                </div>
            </div>
        </div>
        """

        return self._bootstrap_head("Detalle Vehículo") + html + self._bootstrap_footer()

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

    # --- combos bootstrap
    def _get_combo_db_bs(self, tabla, valor, etiqueta, nombre, defecto):
        html = f'<select class="form-select" name="{nombre}">'
        cur = self.con.cursor(dictionary=True)
        cur.execute(f"SELECT {valor},{etiqueta} FROM {tabla}")
        for r in cur.fetchall():
            sel = "selected" if r[valor] == defecto else ""
            html += f'<option value="{r[valor]}" {sel}>{r[etiqueta]}</option>'
        html += "</select>"
        return html

    def _get_combo_anio_bs(self, nombre, inicio, defecto):
        html = f'<select class="form-select" name="{nombre}">'
        actual = datetime.now().year
        try:
            defecto_int = int(defecto) if defecto not in (None, "") else None
        except:
            defecto_int = None

        for i in range(inicio, actual + 1):
            sel = "selected" if defecto_int == i else ""
            html += f'<option value="{i}" {sel}>{i}</option>'
        html += "</select>"
        return html

    def _get_radio_bs(self, arr, nombre, defecto):
        html = '<div class="d-flex flex-wrap gap-3">'
        for v in arr:
            chk = "checked" if v == defecto else ""
            html += f"""
            <div class="form-check">
                <input class="form-check-input" type="radio" name="{nombre}" value="{v}" {chk} required>
                <label class="form-check-label">{v}</label>
            </div>
            """
        html += "</div>"
        return html

    # =====================================================
    # MENSAJES
    # =====================================================
    def _message_error(self, txt):
        return self._bootstrap_head("Error") + f"""
        <div class="container py-4">
            <div class="alert alert-danger shadow-sm text-center">
                <h5 class="mb-1">Error</h5>
                <div>Error al {txt} Favor contactar a ....................</div>
            </div>
            <div class="text-center">
                <a href="?" class="btn btn-secondary">
                    <i class="bi bi-arrow-left"></i> Regresar
                </a>
            </div>
        </div>
        """ + self._bootstrap_footer()

    def _message_ok(self, txt):
        return self._bootstrap_head("OK") + f"""
        <div class="container py-4">
            <div class="alert alert-success shadow-sm text-center">
                <h5 class="mb-1">Correcto</h5>
                <div>El registro se {txt} correctamente</div>
            </div>
            <div class="text-center">
                <a href="?" class="btn btn-primary">
                    <i class="bi bi-list"></i> Regresar a la lista
                </a>
            </div>
        </div>
        """ + self._bootstrap_footer()
