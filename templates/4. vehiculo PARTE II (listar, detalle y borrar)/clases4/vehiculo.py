# class/vehiculo.py
# (equivalente a class/class.vehiculo.php)

import base64
from datetime import datetime

class Vehiculo:

    def __init__(self, cn):
        self.con = cn
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

        print("EJECUTANDOSE EL CONSTRUCTOR VEHICULO\n")

    # =========================================================
    # FORMULARIO (new / update)
    # =========================================================
    def get_form(self, id=None):
        # Código agregado -- //
        if id is None or id == 0:
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
            sql = "SELECT * FROM vehiculo WHERE id=%s;"
            cur = self.con.cursor(dictionary=True)
            cur.execute(sql, (id,))
            row = cur.fetchone()
            bandera = 1 if row else 0

            if not bandera:
                mensaje = f"tratar de actualizar el vehiculo con id= {id} <br>"
                return self._message_error(mensaje)
            else:
                print("\nREGISTRO A MODIFICAR:\n")
                print(row)

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

                # $flag = "disabled";
                flag = ""   # en HTML5 el file input se controla distinto
                op = "update"

        if bandera:
            combustibles = ["Gasolina", "Diesel", "Eléctrico"]

            html = f"""
            <div class="container my-4">
              <div class="card shadow-sm">
                <div class="card-header bg-dark text-white fw-bold">
                  DATOS VEHÍCULO
                </div>
                <div class="card-body">
                  <form name="Form_vehiculo" method="POST" action="index.py" enctype="multipart/form-data">
                    <input type="hidden" name="id" value="{id or 0}">
                    <input type="hidden" name="op" value="{op}">

                    <div class="row g-3">
                      <div class="col-md-4">
                        <label class="form-label">Placa:</label>
                        <input class="form-control" type="text" name="placa" value="{self.placa or ''}" maxlength="10">
                      </div>

                      <div class="col-md-4">
                        <label class="form-label">Marca:</label>
                        {self._get_combo_db("marca","id","descripcion","marca", self.marca)}
                      </div>

                      <div class="col-md-4">
                        <label class="form-label">Motor:</label>
                        <input class="form-control" type="text" name="motor" value="{self.motor or ''}">
                      </div>

                      <div class="col-md-6">
                        <label class="form-label">Chasis:</label>
                        <input class="form-control" type="text" name="chasis" value="{self.chasis or ''}">
                      </div>

                      <div class="col-md-6">
                        <label class="form-label">Combustible:</label>
                        {self._get_radio(combustibles, "combustible", self.combustible)}
                      </div>

                      <div class="col-md-4">
                        <label class="form-label">Año:</label>
                        {self._get_combo_anio("anio",1950, self.anio)}
                      </div>

                      <div class="col-md-4">
                        <label class="form-label">Color:</label>
                        {self._get_combo_db("color","id","descripcion","color", self.color)}
                      </div>

                      <div class="col-md-4">
                        <label class="form-label">Foto:</label>
                        <input class="form-control" type="file" name="foto" {flag}>
                      </div>

                      <div class="col-md-4">
                        <label class="form-label">Avalúo:</label>
                        <input class="form-control" type="text" name="avaluo" value="{self.avaluo or ''}">
                      </div>
                    </div>

                    <div class="mt-4 d-flex gap-2">
                      <button class="btn btn-success" type="submit" name="Guardar" value="GUARDAR">
                        GUARDAR
                      </button>
                      <a class="btn btn-outline-secondary" href="app.py">Regresar</a>
                    </div>
                  </form>
                </div>
              </div>
            </div>
            """
            return html

    # =========================================================
    # LISTA (listar)
    # =========================================================
    def get_list(self):
        d_new = "new/0"                            # Línea agregada
        d_new_final = base64.b64encode(d_new.encode()).decode()  # Línea agregada

        html = f"""
        <div class="container my-4">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h3 class="fw-bold m-0">Lista de Vehículos</h3>
            <button class="btn btn-secondary" disabled>+ Nuevo</button>
          </div>

          <div class="table-responsive">
            <table class="table table-bordered table-hover align-middle">
              <thead class="table-dark">
                <tr>
                  <th>Placa</th>
                  <th>Marca</th>
                  <th>Color</th>
                  <th>Año</th>
                  <th>Avalúo</th>
                  <th colspan="3" class="text-center">Acciones</th>
                </tr>
              </thead>
              <tbody>
        """

        sql = """
            SELECT v.id, v.placa, m.descripcion as marca, c.descripcion as color, v.anio, v.avaluo
            FROM vehiculo v, color c, marca m
            WHERE v.marca=m.id AND v.color=c.id;
        """
        cur = self.con.cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()

        # VERIFICA si existe TUPLAS EN EJECUCION DEL Query
        if rows:
            for row in rows:
                # URL PARA BORRAR
                d_del = f"del/{row['id']}"
                d_del_final = base64.b64encode(d_del.encode()).decode()

                # URL PARA ACTUALIZAR
                d_act = f"act/{row['id']}"
                d_act_final = base64.b64encode(d_act.encode()).decode()

                # URL PARA EL DETALLE
                d_det = f"det/{row['id']}"
                d_det_final = base64.b64encode(d_det.encode()).decode()

                html += f"""
                <tr>
                  <td>{row['placa']}</td>
                  <td>{row['marca']}</td>
                  <td>{row['color']}</td>
                  <td>{row['anio']}</td>
                  <td>${row['avaluo']}</td>

                  <td class="text-center">
                    <a class="btn btn-sm btn-outline-danger"
                       href="app.py?d={d_del_final}"
                       onclick="return confirm('¿Seguro que deseas borrar este registro?');">
                      Borrar
                    </a>
                  </td>

                  <td class="text-center">
                    <button class="btn btn-sm btn-outline-secondary" disabled>Actualizar</button>

                  </td>

                  <td class="text-center">
                    <a class="btn btn-sm btn-outline-info" href="app.py?d={d_det_final}">
                      Detalle
                    </a>
                  </td>
                </tr>
                """
        else:
            mensaje = "Tabla Vehiculo<br>"
            html += f"""
              <tr>
                <td colspan="8" class="text-center">
                  {self._message_BD_Vacia(mensaje)}
                </td>
              </tr>
            """

        html += """
              </tbody>
            </table>
          </div>
        </div>
        """
        return html

    # =========================================================
    # DETALLE
    # =========================================================
    def get_detail_vehiculo(self, id):
        sql = """
            SELECT v.placa, m.descripcion as marca, v.motor, v.chasis, v.combustible,
                   v.anio, c.descripcion as color, v.foto, v.avaluo
            FROM vehiculo v, color c, marca m
            WHERE v.id=%s AND v.marca=m.id AND v.color=c.id;
        """
        cur = self.con.cursor(dictionary=True)
        cur.execute(sql, (id,))
        row = cur.fetchone()

        # VERIFICA SI EXISTE id
        if not row:
            mensaje = f"desplegar el detalle del vehiculo con id= {id} <br>"
            return self._message_error(mensaje)

        print("\nTUPLA\n")
        print(row)

        html = f"""
        <div class="container my-4">
          <div class="card shadow-sm">
            <div class="card-header bg-dark text-white fw-bold">
              DATOS DEL VEHÍCULO
            </div>
            <div class="card-body">
              <table class="table table-bordered">
                <tr><th style="width:180px">Placa</th><td>{row['placa']}</td></tr>
                <tr><th>Marca</th><td>{row['marca']}</td></tr>
                <tr><th>Motor</th><td>{row['motor']}</td></tr>
                <tr><th>Chasis</th><td>{row['chasis']}</td></tr>
                <tr><th>Combustible</th><td>{row['combustible']}</td></tr>
                <tr><th>Año</th><td>{row['anio']}</td></tr>
                <tr><th>Color</th><td>{row['color']}</td></tr>
                <tr><th>Avalúo</th><td><b>${row['avaluo']} USD</b></td></tr>
                <tr><th>Valor Matrícula</th><td><b>${self._calculo_matricula(row['avaluo'])} USD</b></td></tr>
              </table>

              <div class="text-center my-3">
                <img class="img-fluid rounded border"
                     src="static/images/{row['foto']}"
                     style="max-height:320px"
                     alt="foto vehiculo">
              </div>

              <a class="btn btn-outline-secondary" href="app.py">Regresar</a>
            </div>
          </div>
        </div>
        """
        return html

    # =========================================================
    # DELETE
    # =========================================================
    def delete_vehiculo(self, id):
        """
        BORRAR TODOS LOS REGISTROS DE LA BASE DE DATOS (según el id)
        """
        sql = "DELETE FROM vehiculo WHERE id=%s;"
        cur = self.con.cursor()
        try:
            cur.execute(sql, (id,))
            self.con.commit()
            return self._message_ok("eliminó")
        except Exception:
            self.con.rollback()
            return self._message_error("eliminar<br>")

    # =========================================================
    # HELPERS (combos, radio, mensajes)
    # =========================================================
    def _get_combo_db(self, tabla, valor, etiqueta, nombre, defecto=None):
        # _get_combo_db("marca","id","descripcion","marca",$this->marca)
        # _get_combo_db("color","id","descripcion","color", $this->color)

        cur = self.con.cursor(dictionary=True)
        cur.execute(f"SELECT {valor},{etiqueta} FROM {tabla};")
        rows = cur.fetchall()

        html = f'<select class="form-select" name="{nombre}">'
        for row in rows:
            selected = "selected" if defecto == row[valor] else ""
            html += f'<option value="{row[valor]}" {selected}>{row[etiqueta]}</option>\n'
        html += "</select>"
        return html

    def _get_combo_anio(self, nombre, anio_inicial, defecto=None):
        # _get_combo_anio("anio",1950,$this->anio)
        anio_actual = datetime.now().year
        html = f'<select class="form-select" name="{nombre}">'
        for i in range(anio_inicial, anio_actual + 1):
            selected = "selected" if defecto == i else ""
            html += f'<option value="{i}" {selected}>{i}</option>\n'
        html += "</select>"
        return html

    def _get_radio(self, arreglo, nombre, defecto=None):
        # _get_radio($combustibles, "combustible",$this->combustible)
        html = '<div class="d-flex flex-wrap gap-3">'
        for etiqueta in arreglo:
            checked = "checked" if defecto == etiqueta else ""
            html += f"""
              <div class="form-check">
                <input class="form-check-input" type="radio" name="{nombre}" value="{etiqueta}" {checked}>
                <label class="form-check-label">{etiqueta}</label>
              </div>
            """
        html += "</div>"
        return html

    def _calculo_matricula(self, avaluo):
        return f"{float(avaluo) * 0.10:.2f}"

    def _message_error(self, tipo):
        return f"""
        <div class="alert alert-danger text-center">
          <b>Error al {tipo}</b><br>
          Favor contactar a ....................
          <div class="mt-3">
            <a class="btn btn-outline-dark" href="app.py">Regresar</a>
          </div>
        </div>
        """

    def _message_BD_Vacia(self, tipo):
        return f"""
        <div class="alert alert-warning text-center m-0">
          <b>NO existen registros en la {tipo}</b>
          Favor contactar a ....................
        </div>
        """

    def _message_ok(self, tipo):
        return f"""
        <div class="alert alert-success text-center">
          <b>El registro se {tipo} correctamente</b>
          <div class="mt-3">
            <a class="btn btn-outline-dark" href="app.py">Regresar</a>
          </div>
        </div>
        """
