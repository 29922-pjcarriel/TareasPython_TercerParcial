# clases9/producto.py
import os, base64
from werkzeug.utils import secure_filename

def b64_encode(s: str) -> str:
    return base64.b64encode(s.encode("utf-8")).decode("utf-8")

class Producto:
    def __init__(self, conn, upload_folder: str):
        self.conn = conn
        self.upload_folder = upload_folder
        os.makedirs(self.upload_folder, exist_ok=True)

    # ---------- DB ----------
    def list(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM Productos ORDER BY ProductoID DESC")
            return cur.fetchall()

    def get(self, producto_id: int):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM Productos WHERE ProductoID=%s", (producto_id,))
            return cur.fetchone()

    def delete(self, producto_id: int):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM Productos WHERE ProductoID=%s", (producto_id,))

    def save(self, request):
        desc = request.form.get("Descripcion", "").strip()
        precio = request.form.get("Precio", "0").strip()
        det = request.form.get("Detalles", "").strip()

        img = "no-image.png"
        file = request.files.get("Imagen")
        if file and file.filename:
            img = secure_filename(file.filename)
            file.save(os.path.join(self.upload_folder, img))

        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO Productos(Descripcion,Precio,Imagen,Detalles) VALUES(%s,%s,%s,%s)",
                (desc, precio, img, det)
            )

    def update(self, request):
        pid = int(request.form.get("ProductoID", 0))
        desc = request.form.get("Descripcion", "").strip()
        precio = request.form.get("Precio", "0").strip()
        det = request.form.get("Detalles", "").strip()
        img_actual = request.form.get("ImagenActual", "no-image.png")

        img = img_actual
        file = request.files.get("Imagen")
        if file and file.filename:
            img = secure_filename(file.filename)
            file.save(os.path.join(self.upload_folder, img))

        with self.conn.cursor() as cur:
            cur.execute(
                """UPDATE Productos
                   SET Descripcion=%s, Precio=%s, Imagen=%s, Detalles=%s
                   WHERE ProductoID=%s""",
                (desc, precio, img, det, pid)
            )

    # ---------- HTML helpers ----------
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
</body>
</html>"""

    # ---------- HTML pages (como en PHP dentro de clase) ----------
    def html_list(self) -> str:
        rows = ""
        for pr in self.list():
            rows += f"""
            <tr>
              <td><img class="img-thumbnail" style="width:90px"
                   src="/static/images/productos/{pr['Imagen']}" alt=""></td>
              <td>{pr['Descripcion']}</td>
              <td>${float(pr['Precio']):.2f}</td>
              <td>{pr['Detalles']}</td>
              <td><a class="btn btn-sm btn-outline-danger"
                     href="/?d={b64_encode('pdel/'+str(pr['ProductoID']))}">Borrar</a></td>
              <td><a class="btn btn-sm btn-outline-warning"
                     href="/?d={b64_encode('pact/'+str(pr['ProductoID']))}">Actualizar</a></td>
              <td><a class="btn btn-sm btn-outline-info"
                     href="/?d={b64_encode('pdet/'+str(pr['ProductoID']))}">Detalle</a></td>
            </tr>
            """
        body = f"""
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h4 class="m-0">Lista de Productos</h4>
          <a class="btn btn-success" href="/?d={b64_encode('pnew/0')}">Nuevo</a>
        </div>
        <div class="card shadow-sm">
          <div class="table-responsive">
            <table class="table table-striped table-hover align-middle mb-0">
              <thead class="table-dark">
                <tr>
                  <th>Imagen</th><th>Descripción</th><th>Precio</th><th>Detalles</th>
                  <th colspan="3">Acciones</th>
                </tr>
              </thead>
              <tbody>{rows}</tbody>
            </table>
          </div>
        </div>
        """
        return self._layout("Productos", body)

    def html_form_new(self) -> str:
        return self._layout("Nuevo Producto", self._form_html(modo="new", producto=None))

    def html_form_update(self, producto_id: int) -> str:
        return self._layout("Actualizar Producto", self._form_html(modo="update", producto=self.get(producto_id)))

    def _form_html(self, modo: str, producto):
        if modo == "new":
            op = "pnew"
            pid = 0
            desc = ""
            precio = ""
            det = ""
            img = "no-image.png"
            titulo = "Nuevo Producto"
        else:
            op = "pupdate"
            pid = producto["ProductoID"]
            desc = producto["Descripcion"]
            precio = producto["Precio"]
            det = producto["Detalles"]
            img = producto["Imagen"]
            titulo = "Actualizar Producto"

        return f"""
        <div class="card shadow-sm">
          <div class="card-header bg-dark text-white"><b>{titulo}</b></div>
          <div class="card-body">
            <form method="POST" action="/" enctype="multipart/form-data">
              <input type="hidden" name="op" value="{op}">
              <input type="hidden" name="ProductoID" value="{pid}">
              <input type="hidden" name="ImagenActual" value="{img}">

              <div class="mb-3">
                <label class="form-label">Descripción</label>
                <input class="form-control" name="Descripcion" required value="{desc}">
              </div>

              <div class="mb-3">
                <label class="form-label">Precio</label>
                <input class="form-control" name="Precio" required value="{precio}">
              </div>

              <div class="mb-3">
                <label class="form-label">Detalles</label>
                <input class="form-control" name="Detalles" required value="{det}">
              </div>

              <div class="mb-3">
                <label class="form-label">Imagen</label>
                <input class="form-control" type="file" name="Imagen">
                <div class="mt-2">
                  <img class="img-thumbnail" style="width:200px"
                       src="/static/images/productos/{img}" alt="">
                </div>
              </div>

              <div class="d-flex gap-2">
                <button class="btn btn-primary" type="submit" name="Guardar">GUARDAR</button>
                <a class="btn btn-outline-secondary" href="/?d={b64_encode('plist/0')}">Regresar</a>
              </div>
            </form>
          </div>
        </div>
        """

    def html_detail(self, producto_id: int) -> str:
        p = self.get(producto_id)
        body = f"""
        <div class="card shadow-sm">
          <div class="card-header bg-dark text-white"><b>Detalle Producto</b></div>
          <div class="card-body">
            <div class="row g-3">
              <div class="col-md-4">
                <img class="img-fluid img-thumbnail"
                     src="/static/images/productos/{p['Imagen']}" alt="">
              </div>
              <div class="col-md-8">
                <p><b>Descripción:</b> {p['Descripcion']}</p>
                <p><b>Precio:</b> ${float(p['Precio']):.2f}</p>
                <p><b>Detalles:</b> {p['Detalles']}</p>
                <a class="btn btn-outline-secondary" href="/?d={b64_encode('plist/0')}">Regresar</a>
              </div>
            </div>
          </div>
        </div>
        """
        return self._layout("Detalle Producto", body)
