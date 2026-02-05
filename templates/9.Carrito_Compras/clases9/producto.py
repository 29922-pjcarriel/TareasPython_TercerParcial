# class/producto.py
import os
from werkzeug.utils import secure_filename
from flask import request

class Producto:
    def __init__(self, cn, img_dir_abs: str):
        self.cn = cn
        self.img_dir_abs = img_dir_abs

    def _ok(self, msg):
        return f"<div class='alert alert-success'>✅ {msg}</div>"

    def _err(self, msg):
        return f"<div class='alert alert-danger'>❌ {msg}</div>"

    def get_list(self, U, IMG):
        cur = self.cn.cursor(dictionary=True)
        cur.execute("SELECT * FROM Productos ORDER BY ProductoID DESC")
        rows = cur.fetchall()

        html = f"""
        <h2>Productos</h2>
        <div class="mb-3 text-end">
          <a class="btn btn-success" href="{U('pnew/0')}">Nuevo</a>
        </div>

        <div class="table-responsive">
        <table class="table table-striped table-hover align-middle">
          <thead class="table-dark">
            <tr>
              <th>ID</th><th>Descripción</th><th>Precio</th><th>Imagen</th><th>Detalles</th>
              <th class="text-center">Detalle</th>
              <th class="text-center">Actualizar</th>
              <th class="text-center">Borrar</th>
            </tr>
          </thead>
          <tbody>
        """

        for r in rows:
            pid = int(r["ProductoID"])
            img = (r.get("Imagen") or "no-image.png")
            html += f"""
            <tr>
              <td>{pid}</td>
              <td>{r.get("Descripcion","")}</td>
              <td>{r.get("Precio","")}</td>
              <td><img src="{IMG(img)}" style="max-height:60px"></td>
              <td>{r.get("Detalles","")}</td>
              <td class="text-center"><a class="btn btn-info btn-sm" href="{U(f"pdet/{pid}")}">Detalle</a></td>
              <td class="text-center"><a class="btn btn-warning btn-sm" href="{U(f"pact/{pid}")}">Actualizar</a></td>
              <td class="text-center">
                <a class="btn btn-danger btn-sm" href="{U(f"pdel/{pid}")}" onclick="return confirm('¿Eliminar este producto?');">Borrar</a>
              </td>
            </tr>
            """

        html += "</tbody></table></div>"
        return html

    def get_form(self, U, IMG, pid=0):
        pid = int(pid)
        data = {"ProductoID": 0, "Descripcion": "", "Precio": "", "Imagen": "no-image.png", "Detalles": ""}

        if pid > 0:
            cur = self.cn.cursor(dictionary=True)
            cur.execute("SELECT * FROM Productos WHERE ProductoID=%s", (pid,))
            row = cur.fetchone()
            if row:
                data.update(row)

        op = "pnew" if pid == 0 else "pupdate"
        titulo = "Nuevo Producto" if pid == 0 else "Actualizar Producto"

        return f"""
        <h2>{titulo}</h2>

        <form method="POST" enctype="multipart/form-data">
          <input type="hidden" name="op" value="{op}">
          <input type="hidden" name="ProductoID" value="{data["ProductoID"]}">

          <div class="mb-3">
            <label class="form-label">Descripción</label>
            <input class="form-control" name="Descripcion" value="{data.get("Descripcion","")}" required>
          </div>

          <div class="mb-3">
            <label class="form-label">Precio</label>
            <input class="form-control" name="Precio" type="number" step="0.01" value="{data.get("Precio","")}" required>
          </div>

          <div class="mb-3">
            <label class="form-label">Detalles</label>
            <input class="form-control" name="Detalles" value="{data.get("Detalles","")}" required>
          </div>

          <div class="mb-3">
            <label class="form-label">Imagen (opcional)</label>
            <input class="form-control" type="file" name="Imagen" accept="image/*">
            <div class="mt-2">
              <small>Actual:</small><br>
              <img src="{IMG(data.get("Imagen") or "no-image.png")}" style="max-height:90px">
            </div>
          </div>

          <button class="btn btn-primary" type="submit" name="Guardar" value="1">Guardar</button>
          <a class="btn btn-secondary" href="{U("plist/0")}">Volver</a>
        </form>
        """

    def get_detail(self, U, IMG, pid):
        pid = int(pid)
        cur = self.cn.cursor(dictionary=True)
        cur.execute("SELECT * FROM Productos WHERE ProductoID=%s", (pid,))
        r = cur.fetchone()
        if not r:
            return "<div class='alert alert-warning'>Producto no encontrado.</div>"

        img = (r.get("Imagen") or "no-image.png")

        return f"""
        <h2>Detalle Producto</h2>
        <div class="card p-3">
          <h5>{r.get("Descripcion","")}</h5>
          <p><b>Precio:</b> {r.get("Precio","")}</p>
          <p><b>Detalles:</b> {r.get("Detalles","")}</p>
          <img src="{IMG(img)}" style="max-height:160px; width:auto;">
        </div>

        <div class="mt-3">
          <a class="btn btn-secondary" href="{U("plist/0")}">Volver</a>
        </div>
        """

    def delete(self, U, pid):
        pid = int(pid)
        try:
            cur = self.cn.cursor()
            cur.execute("DELETE FROM Productos WHERE ProductoID=%s", (pid,))
            return self._ok("Producto eliminado.") + f"<a class='btn btn-secondary' href='{U('plist/0')}'>Volver</a>"
        except Exception as e:
            return self._err(f"No se pudo eliminar: {e}")

    def save(self, U):
        try:
            desc = request.form.get("Descripcion", "")
            precio = request.form.get("Precio", "0")
            det = request.form.get("Detalles", "")

            img_name = "no-image.png"
            f = request.files.get("Imagen")

            if f and f.filename:
                os.makedirs(self.img_dir_abs, exist_ok=True)
                img_name = secure_filename(f.filename)
                f.save(os.path.join(self.img_dir_abs, img_name))

            cur = self.cn.cursor()
            cur.execute(
                "INSERT INTO Productos (Descripcion, Precio, Imagen, Detalles) VALUES (%s,%s,%s,%s)",
                (desc, precio, img_name, det)
            )
            return self._ok("Producto guardado.") + f"<a class='btn btn-secondary' href='{U('plist/0')}'>Volver</a>"
        except Exception as e:
            return self._err(f"No se pudo guardar: {e}")

    def update(self, U):
        try:
            pid = int(request.form.get("ProductoID", "0"))
            desc = request.form.get("Descripcion", "")
            precio = request.form.get("Precio", "0")
            det = request.form.get("Detalles", "")

            cur = self.cn.cursor(dictionary=True)
            cur.execute("SELECT Imagen FROM Productos WHERE ProductoID=%s", (pid,))
            row = cur.fetchone()
            img_name = (row.get("Imagen") if row else "no-image.png") or "no-image.png"

            f = request.files.get("Imagen")
            if f and f.filename:
                os.makedirs(self.img_dir_abs, exist_ok=True)
                img_name = secure_filename(f.filename)
                f.save(os.path.join(self.img_dir_abs, img_name))

            cur2 = self.cn.cursor()
            cur2.execute(
                "UPDATE Productos SET Descripcion=%s, Precio=%s, Imagen=%s, Detalles=%s WHERE ProductoID=%s",
                (desc, precio, img_name, det, pid)
            )
            return self._ok("Producto actualizado.") + f"<a class='btn btn-secondary' href='{U('plist/0')}'>Volver</a>"
        except Exception as e:
            return self._err(f"No se pudo actualizar: {e}")
