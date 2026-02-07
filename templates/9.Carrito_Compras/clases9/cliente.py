# class/cliente.py
from flask import request

class Cliente:
    def __init__(self, cn):
        self.cn = cn

    def _ok(self, msg):
        return f"<div class='alert alert-success'>✅ {msg}</div>"

    def _err(self, msg):
        return f"<div class='alert alert-danger'>❌ {msg}</div>"

    def get_list(self, U):
        cur = self.cn.cursor(dictionary=True)
        cur.execute("SELECT * FROM Clientes ORDER BY ClienteID DESC")
        rows = cur.fetchall()

        html = f"""
        <h2>Clientes</h2>
        <div class="mb-3 text-end">
          <a class="btn btn-success" href="{U('cnew/0')}">Nuevo</a>
        </div>

        <div class="table-responsive">
        <table class="table table-striped table-hover align-middle">
          <thead class="table-dark">
            <tr>
              <th>ID</th><th>Razón Social</th><th>Ciudad</th><th>Teléfonos</th>
              <th class="text-center">Detalle</th>
              <th class="text-center">Actualizar</th>
              <th class="text-center">Borrar</th>
            </tr>
          </thead>
          <tbody>
        """

        for r in rows:
            cid = int(r["ClienteID"])
            html += f"""
            <tr>
              <td>{cid}</td>
              <td>{r.get("RazonSocial","")}</td>
              <td>{r.get("Ciudad","")}</td>
              <td>{r.get("Telefonos","")}</td>
              <td class="text-center"><a class="btn btn-info btn-sm" href="{U(f"cdet/{cid}")}">Detalle</a></td>
              <td class="text-center"><a class="btn btn-warning btn-sm" href="{U(f"cact/{cid}")}">Actualizar</a></td>
              <td class="text-center">
                <a class="btn btn-danger btn-sm" href="{U(f"cdel/{cid}")}" onclick="return confirm('¿Eliminar este cliente?');">Borrar</a>
              </td>
            </tr>
            """

        html += "</tbody></table></div>"
        return html

    def get_form(self, U, cid=0):
        cid = int(cid)
        data = {
            "ClienteID": 0, "RazonSocial": "", "Direccion": "", "Ciudad": "", "Estado": "",
            "CodigoPostal": "", "Rif": "", "Pais": "", "Telefonos": ""
        }

        if cid > 0:
            cur = self.cn.cursor(dictionary=True)
            cur.execute("SELECT * FROM Clientes WHERE ClienteID=%s", (cid,))
            row = cur.fetchone()
            if row:
                data.update(row)

        op = "cnew" if cid == 0 else "cupdate"
        titulo = "Nuevo Cliente" if cid == 0 else "Actualizar Cliente"

        return f"""
        <h2>{titulo}</h2>

        <form method="POST">
          <input type="hidden" name="op" value="{op}">
          <input type="hidden" name="ClienteID" value="{data["ClienteID"]}">

          <div class="mb-3"><label class="form-label">Razón Social</label>
            <input class="form-control" name="RazonSocial" value="{data.get("RazonSocial","")}" required>
          </div>

          <div class="mb-3"><label class="form-label">Dirección</label>
            <input class="form-control" name="Direccion" value="{data.get("Direccion","")}">
          </div>

          <div class="mb-3"><label class="form-label">Ciudad</label>
            <input class="form-control" name="Ciudad" value="{data.get("Ciudad","")}">
          </div>

          <div class="mb-3"><label class="form-label">Estado</label>
            <input class="form-control" name="Estado" value="{data.get("Estado","")}">
          </div>

          <div class="mb-3"><label class="form-label">Código Postal</label>
            <input class="form-control" name="CodigoPostal" value="{data.get("CodigoPostal","")}">
          </div>

          <div class="mb-3"><label class="form-label">RIF</label>
            <input class="form-control" name="Rif" value="{data.get("Rif","")}">
          </div>

          <div class="mb-3"><label class="form-label">País</label>
            <input class="form-control" name="Pais" value="{data.get("Pais","")}">
          </div>

          <div class="mb-3"><label class="form-label">Teléfonos</label>
            <input class="form-control" name="Telefonos" value="{data.get("Telefonos","")}">
          </div>

          <button class="btn btn-primary" type="submit" name="Guardar" value="1">Guardar</button>
          <a class="btn btn-secondary" href="{U("clist/0")}">Volver</a>
        </form>
        """

    def get_detail(self, U, cid):
        cid = int(cid)
        cur = self.cn.cursor(dictionary=True)
        cur.execute("SELECT * FROM Clientes WHERE ClienteID=%s", (cid,))
        r = cur.fetchone()
        if not r:
            return "<div class='alert alert-warning'>Cliente no encontrado.</div>"

        return f"""
        <h2>Detalle Cliente</h2>
        <div class="card p-3">
          <p><b>Razón Social:</b> {r.get("RazonSocial","")}</p>
          <p><b>Dirección:</b> {r.get("Direccion","")}</p>
          <p><b>Ciudad:</b> {r.get("Ciudad","")}</p>
          <p><b>Estado:</b> {r.get("Estado","")}</p>
          <p><b>Teléfonos:</b> {r.get("Telefonos","")}</p>
        </div>

        <div class="mt-3">
          <a class="btn btn-secondary" href="{U("clist/0")}">Volver</a>
        </div>
        """

    def delete(self, U, cid):
        cid = int(cid)
        try:
            cur = self.cn.cursor()
            cur.execute("DELETE FROM Clientes WHERE ClienteID=%s", (cid,))
            return self._ok("Cliente eliminado.") + f"<a class='btn btn-secondary' href='{U('clist/0')}'>Volver</a>"
        except Exception as e:
            return self._err(f"No se pudo eliminar: {e}")

    def save(self, U):
        try:
            f = request.form
            cur = self.cn.cursor()
            cur.execute("""
                INSERT INTO Clientes (RazonSocial, Direccion, Ciudad, Estado, CodigoPostal, Rif, Pais, Telefonos)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                f.get("RazonSocial"), f.get("Direccion"), f.get("Ciudad"), f.get("Estado"),
                f.get("CodigoPostal"), f.get("Rif"), f.get("Pais"), f.get("Telefonos")
            ))
            return self._ok("Cliente guardado.") + f"<a class='btn btn-secondary' href='{U('clist/0')}'>Volver</a>"
        except Exception as e:
            return self._err(f"No se pudo guardar: {e}")

    def update(self, U):
        try:
            f = request.form
            cid = int(f.get("ClienteID", "0"))
            cur = self.cn.cursor()
            cur.execute("""
                UPDATE Clientes SET
                  RazonSocial=%s, Direccion=%s, Ciudad=%s, Estado=%s, CodigoPostal=%s, Rif=%s, Pais=%s, Telefonos=%s
                WHERE ClienteID=%s
            """, (
                f.get("RazonSocial"), f.get("Direccion"), f.get("Ciudad"), f.get("Estado"),
                f.get("CodigoPostal"), f.get("Rif"), f.get("Pais"), f.get("Telefonos"), cid
            ))
            return self._ok("Cliente actualizado.") + f"<a class='btn btn-secondary' href='{U('clist/0')}'>Volver</a>"
        except Exception as e:
            return self._err(f"No se pudo actualizar: {e}")
