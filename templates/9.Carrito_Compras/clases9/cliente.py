# clases9/cliente.py
import base64

def b64_encode(s: str) -> str:
    return base64.b64encode(s.encode("utf-8")).decode("utf-8")

class Cliente:
    def __init__(self, conn):
        self.conn = conn

    # ---------- DB ----------
    def list(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM Clientes ORDER BY ClienteID DESC")
            return cur.fetchall()

    def get(self, cliente_id: int):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM Clientes WHERE ClienteID=%s", (cliente_id,))
            return cur.fetchone()

    def delete(self, cliente_id: int):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM Clientes WHERE ClienteID=%s", (cliente_id,))

    def save(self, f):
        with self.conn.cursor() as cur:
            cur.execute(
                """INSERT INTO Clientes
                   (RazonSocial,Direccion,Ciudad,Estado,CodigoPostal,Rif,Pais,Telefonos)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    f.get("RazonSocial"), f.get("Direccion"), f.get("Ciudad"), f.get("Estado"),
                    f.get("CodigoPostal"), f.get("Rif"), f.get("Pais"), f.get("Telefonos")
                )
            )

    def update(self, f):
        cid = int(f.get("ClienteID", 0))
        with self.conn.cursor() as cur:
            cur.execute(
                """UPDATE Clientes SET
                   RazonSocial=%s, Direccion=%s, Ciudad=%s, Estado=%s,
                   CodigoPostal=%s, Rif=%s, Pais=%s, Telefonos=%s
                   WHERE ClienteID=%s""",
                (
                    f.get("RazonSocial"), f.get("Direccion"), f.get("Ciudad"), f.get("Estado"),
                    f.get("CodigoPostal"), f.get("Rif"), f.get("Pais"), f.get("Telefonos"), cid
                )
            )

    # ---------- HTML (layout igual) ----------
    def _layout(self, title: str, body: str) -> str:
        nav = f"""
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
          <div class="container">
            <a class="navbar-brand fw-bold" href="/">Carrito CRUD</a>
            <div class="d-flex gap-2">
              <a class="btn btn-outline-light btn-sm" href="/?d={b64_encode('olist/0')}">Pedidos</a>
              <a class="btn btn-outline-light btn-sm" href="/?d={b64_encode('plist/0')}">Productos</a>
              <a class="btn btn-outline-light btn-sm" href="/?d={b64_encode('clist/0')}">Clientes</a>
            </div>
          </div>
        </nav>
        """
        return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
{nav}
<div class="container my-4">{body}</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body></html>"""

    def html_list(self) -> str:
        rows = ""
        for c in self.list():
            rows += f"""
            <tr>
              <td>{c['RazonSocial'] or ''}</td>
              <td>{c['Ciudad'] or ''}</td>
              <td>{c['Pais'] or ''}</td>
              <td>{c['Telefonos'] or ''}</td>
              <td><a class="btn btn-sm btn-outline-danger"
                     href="/?d={b64_encode('cdel/'+str(c['ClienteID']))}">Borrar</a></td>
              <td><a class="btn btn-sm btn-outline-warning"
                     href="/?d={b64_encode('cact/'+str(c['ClienteID']))}">Actualizar</a></td>
              <td><a class="btn btn-sm btn-outline-info"
                     href="/?d={b64_encode('cdet/'+str(c['ClienteID']))}">Detalle</a></td>
            </tr>
            """
        body = f"""
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h4 class="m-0">Lista de Clientes</h4>
          <a class="btn btn-success" href="/?d={b64_encode('cnew/0')}">Nuevo</a>
        </div>
        <div class="card shadow-sm">
          <div class="table-responsive">
            <table class="table table-striped table-hover align-middle mb-0">
              <thead class="table-dark">
                <tr>
                  <th>Razón Social</th><th>Ciudad</th><th>País</th><th>Teléfonos</th>
                  <th colspan="3">Acciones</th>
                </tr>
              </thead>
              <tbody>{rows}</tbody>
            </table>
          </div>
        </div>
        """
        return self._layout("Clientes", body)

    def html_form_new(self) -> str:
        return self._layout("Nuevo Cliente", self._form_html("new", None))

    def html_form_update(self, cliente_id: int) -> str:
        return self._layout("Actualizar Cliente", self._form_html("update", self.get(cliente_id)))

    def _form_html(self, modo: str, c):
        if modo == "new":
            op = "cnew"
            cid = 0
            data = {"RazonSocial":"", "Rif":"", "Direccion":"", "Ciudad":"", "Estado":"",
                    "CodigoPostal":"", "Pais":"", "Telefonos":""}
            titulo = "Nuevo Cliente"
        else:
            op = "cupdate"
            cid = c["ClienteID"]
            data = c
            titulo = "Actualizar Cliente"

        return f"""
        <div class="card shadow-sm">
          <div class="card-header bg-dark text-white"><b>{titulo}</b></div>
          <div class="card-body">
            <form method="POST" action="/">
              <input type="hidden" name="op" value="{op}">
              <input type="hidden" name="ClienteID" value="{cid}">

              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Razón Social</label>
                  <input class="form-control" name="RazonSocial" value="{data.get('RazonSocial','') or ''}">
                </div>
                <div class="col-md-6">
                  <label class="form-label">RIF</label>
                  <input class="form-control" name="Rif" value="{data.get('Rif','') or ''}">
                </div>
                <div class="col-md-12">
                  <label class="form-label">Dirección</label>
                  <input class="form-control" name="Direccion" value="{data.get('Direccion','') or ''}">
                </div>
                <div class="col-md-4">
                  <label class="form-label">Ciudad</label>
                  <input class="form-control" name="Ciudad" value="{data.get('Ciudad','') or ''}">
                </div>
                <div class="col-md-4">
                  <label class="form-label">Estado</label>
                  <input class="form-control" name="Estado" value="{data.get('Estado','') or ''}">
                </div>
                <div class="col-md-4">
                  <label class="form-label">Código Postal</label>
                  <input class="form-control" name="CodigoPostal" value="{data.get('CodigoPostal','') or ''}">
                </div>
                <div class="col-md-6">
                  <label class="form-label">País</label>
                  <input class="form-control" name="Pais" value="{data.get('Pais','') or ''}">
                </div>
                <div class="col-md-6">
                  <label class="form-label">Teléfonos</label>
                  <input class="form-control" name="Telefonos" value="{data.get('Telefonos','') or ''}">
                </div>
              </div>

              <div class="d-flex gap-2 mt-3">
                <button class="btn btn-primary" type="submit" name="Guardar">GUARDAR</button>
                <a class="btn btn-outline-secondary" href="/?d={b64_encode('clist/0')}">Regresar</a>
              </div>
            </form>
          </div>
        </div>
        """

    def html_detail(self, cliente_id: int) -> str:
        c = self.get(cliente_id)
        body = f"""
        <div class="card shadow-sm">
          <div class="card-header bg-dark text-white"><b>Detalle Cliente</b></div>
          <div class="card-body">
            <p><b>Razón Social:</b> {c['RazonSocial'] or ''}</p>
            <p><b>Dirección:</b> {c['Direccion'] or ''}</p>
            <p><b>Ciudad:</b> {c['Ciudad'] or ''}</p>
            <p><b>País:</b> {c['Pais'] or ''}</p>
            <p><b>Teléfonos:</b> {c['Telefonos'] or ''}</p>
            <a class="btn btn-outline-secondary" href="/?d={b64_encode('clist/0')}">Regresar</a>
          </div>
        </div>
        """
        return self._layout("Detalle Cliente", body)
