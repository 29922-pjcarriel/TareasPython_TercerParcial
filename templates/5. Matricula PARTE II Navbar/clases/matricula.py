# clases/matricula.py
# (equivalente a class/class.matricula.php)

import base64

class Matricula:

    def __init__(self, cn):
        self.con = cn
        self.id = None
        self.fecha = None
        self.vehiculo = None
        self.agencia = None
        self.anio = None

        # print("EJECUTANDOSE EL CONSTRUCTOR MATRICULA\n")

    # =========================================================
    # LISTA (listar)
    # =========================================================
    def get_list(self):
        # Se deja como en PHP, pero deshabilitado visualmente
        d_new = "new/0"
        d_new_final = base64.b64encode(d_new.encode()).decode()

        html = f"""
        <div class="container my-4">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h3 class="fw-bold m-0">Lista de Matrículas</h3>
            <button class="btn btn-secondary" disabled>+ Nuevo</button>
          </div>

          <div class="table-responsive">
            <table class="table table-striped table-bordered table-hover text-center align-middle">
              <thead class="table-dark">
                <tr>
                  <th>Fecha</th>
                  <th>Vehículo (Placa)</th>
                  <th>Agencia (Descripción)</th>
                  <th>Año</th>
                  <th colspan="3">Acciones</th>
                </tr>
              </thead>
              <tbody>
        """

        sql = """
            SELECT m.id, m.fecha, v.placa as vehiculo, a.descripcion as agencia, m.anio
            FROM matricula m, vehiculo v, agencia a
            WHERE m.vehiculo=v.id AND m.agencia=a.id;
        """
        cur = self.con.cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()

        if rows:
            for row in rows:
                # URL PARA BORRAR
                d_del = f"del/{row['id']}"
                d_del_final = base64.b64encode(d_del.encode()).decode()

                # URL PARA ACTUALIZAR (deshabilitado)
                d_act = f"act/{row['id']}"
                d_act_final = base64.b64encode(d_act.encode()).decode()

                # URL PARA EL DETALLE
                d_det = f"det/{row['id']}"
                d_det_final = base64.b64encode(d_det.encode()).decode()

                html += f"""
                <tr>
                  <td>{row['fecha']}</td>
                  <td>{row['vehiculo']}</td>
                  <td>{row['agencia']}</td>
                  <td>{row['anio']}</td>

                  <td>
                    <a class="btn btn-sm btn-outline-danger"
                       href="app.py?mod=matricula&d={d_del_final}"
                       onclick="return confirm('¿Seguro que deseas borrar esta matrícula?');">
                      Borrar
                    </a>
                  </td>

                  <td>
                    <button class="btn btn-sm btn-outline-secondary" disabled>
                      Actualizar
                    </button>
                  </td>

                  <td>
                    <a class="btn btn-sm btn-outline-info"
                       href="app.py?mod=matricula&d={d_det_final}">
                      Detalle
                    </a>
                  </td>
                </tr>
                """
        else:
            mensaje = "Tabla Matricula<br>"
            html += f"""
              <tr>
                <td colspan="7" class="text-center">
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
    def get_detail_matricula(self, id):
        sql = """
            SELECT m.fecha, v.placa as vehiculo, a.descripcion as agencia, m.anio
            FROM matricula m, vehiculo v, agencia a
            WHERE m.id=%s AND m.vehiculo=v.id AND m.agencia=a.id;
        """
        cur = self.con.cursor(dictionary=True)
        cur.execute(sql, (id,))
        row = cur.fetchone()

        if not row:
            mensaje = f"desplegar el detalle de la matricula con id= {id} <br>"
            return self._message_error(mensaje, back="app.py?mod=matricula")

        # print("\nTUPLA\n")
        # print(row)

        html = f"""
        <div class="container my-4">
          <div class="row justify-content-center">
            <div class="col-md-7 col-lg-6">
              <div class="card shadow-sm">
                <div class="card-header bg-success text-white text-center fw-bold">
                  Detalle Matrícula
                </div>

                <div class="card-body p-0">
                  <table class="table table-bordered mb-0">
                    <tr>
                      <th class="bg-light w-50">Fecha</th>
                      <td>{row['fecha']}</td>
                    </tr>
                    <tr>
                      <th class="bg-light">Vehículo (Placa)</th>
                      <td>{row['vehiculo']}</td>
                    </tr>
                    <tr>
                      <th class="bg-light">Agencia (Descripción)</th>
                      <td>{row['agencia']}</td>
                    </tr>
                    <tr>
                      <th class="bg-light">Año</th>
                      <td>{row['anio']}</td>
                    </tr>
                  </table>
                </div>

                <div class="card-footer text-center">
                  <a href="app.py?mod=matricula" class="btn btn-secondary">
                    Regresar
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
        """
        return html

    # =========================================================
    # DELETE
    # =========================================================
    def delete_matricula(self, id):
        sql = "DELETE FROM matricula WHERE id=%s;"
        cur = self.con.cursor()
        try:
            cur.execute(sql, (id,))
            self.con.commit()
            return self._message_ok("eliminó", back="app.py?mod=matricula")
        except Exception:
            self.con.rollback()
            return self._message_error("eliminar<br>", back="app.py?mod=matricula")

    # =========================================================
    # MENSAJES (igual estilo que Vehiculo)
    # =========================================================
    def _message_error(self, tipo, back="app.py?mod=matricula"):
        return f"""
        <div class="container my-4">
          <div class="alert alert-danger text-center">
            <b>Error al {tipo}</b><br>
            Favor contactar a ....................
            <div class="mt-3">
              <a class="btn btn-outline-dark" href="{back}">Regresar</a>
            </div>
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

    def _message_ok(self, tipo, back="app.py?mod=matricula"):
        return f"""
        <div class="container my-4">
          <div class="alert alert-success text-center">
            <b>El registro se {tipo} correctamente</b>
            <div class="mt-3">
              <a class="btn btn-outline-dark" href="{back}">Regresar</a>
            </div>
          </div>
        </div>
        """
