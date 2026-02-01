# clases9/pedido.py
import base64
from datetime import datetime

def b64_encode(s: str) -> str:
    return base64.b64encode(s.encode("utf-8")).decode("utf-8")

class Pedido:
    def __init__(self, conn):
        self.conn = conn

    # ---------- DB ----------
    def list(self):
        sql = """SELECT p.PedidoID, p.FechaPedido, c.RazonSocial
                 FROM Pedidos p
                 LEFT JOIN Clientes c ON c.ClienteID=p.ClienteID
                 ORDER BY p.PedidoID DESC"""
        with self.conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

    def get(self, pedido_id: int):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM Pedidos WHERE PedidoID=%s", (pedido_id,))
            return cur.fetchone()

    def delete(self, pedido_id: int):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM PedidosItems WHERE PedidoID=%s", (pedido_id,))
            cur.execute("DELETE FROM Pedidos WHERE PedidoID=%s", (pedido_id,))

    def save(self, f):
        cliente_id = int(f.get("ClienteID", 0))
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO Pedidos(ClienteID, FechaPedido) VALUES(%s,%s)", (cliente_id, fecha))
            return cur.lastrowid

    def update(self, f):
        pid = int(f.get("PedidoID", 0))
        cid = int(f.get("ClienteID", 0))
        with self.conn.cursor() as cur:
            cur.execute("UPDATE Pedidos SET ClienteID=%s WHERE PedidoID=%s", (cid, pid))

    # ---------- ITEMS ----------
    def items(self, pedido_id: int):
        sql = """SELECT i.ProductoID, i.Cantidad, p.Descripcion, p.Precio, p.Imagen
                 FROM PedidosItems i
                 JOIN Productos p ON p.ProductoID=i.ProductoID
                 WHERE i.PedidoID=%s
                 ORDER BY p.ProductoID DESC"""
        with self.conn.cursor() as cur:
            cur.execute(sql, (pedido_id,))
            data = cur.fetchall()

        total = 0
        for it in data:
            it["Subtotal"] = float(it["Precio"]) * int(it["Cantidad"])
            total += it["Subtotal"]
        return data, total

    def add_item(self, pedido_id: int, producto_id: int):
        with self.conn.cursor() as cur:
            cur.execute("""SELECT Cantidad FROM PedidosItems
                           WHERE PedidoID=%s AND ProductoID=%s""", (pedido_id, producto_id))
            row = cur.fetchone()
            if row:
                cur.execute("""UPDATE PedidosItems SET Cantidad=Cantidad+1
                               WHERE PedidoID=%s AND ProductoID=%s""", (pedido_id, producto_id))
            else:
                cur.execute("""INSERT INTO PedidosItems(PedidoID,ProductoID,Cantidad)
                               VALUES(%s,%s,1)""", (pedido_id, producto_id))

    def rm_item(self, pedido_id: int, producto_id: int):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM PedidosItems WHERE PedidoID=%s AND ProductoID=%s", (pedido_id, producto_id))

    def clear_items(self, pedido_id: int):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM PedidosItems WHERE PedidoID=%s", (pedido_id,))

    def update_qty(self, form):
        pedido_id = int(form.get("PedidoID", 0))
        for key, val in form.items():
            if key.startswith("qty[") and key.endswith("]"):
                producto_id = int(key[4:-1])
                qty = int(val or 0)
                with self.conn.cursor() as cur:
                    if qty <= 0:
                        cur.execute("DELETE FROM PedidosItems WHERE PedidoID=%s AND ProductoID=%s",
                                    (pedido_id, producto_id))
                    else:
                        cur.execute("""UPDATE PedidosItems SET Cantidad=%s
                                       WHERE PedidoID=%s AND ProductoID=%s""",
                                    (qty, pedido_id, producto_id))
        return pedido_id

    def detail(self, pedido_id: int):
        with self.conn.cursor() as cur:
            cur.execute("""SELECT p.FechaPedido, c.RazonSocial
                           FROM Pedidos p
                           LEFT JOIN Clientes c ON c.ClienteID=p.ClienteID
                           WHERE p.PedidoID=%s""", (pedido_id,))
            cab = cur.fetchone()

            cur.execute("""SELECT i.Cantidad, pr.Descripcion, pr.Precio
                           FROM PedidosItems i
                           JOIN Productos pr ON pr.ProductoID=i.ProductoID
                           WHERE i.PedidoID=%s""", (pedido_id,))
            det = cur.fetchall()

        total = 0
        for d in det:
            d["Subtotal"] = float(d["Precio"]) * int(d["Cantidad"])
            total += d["Subtotal"]
        return cab, det, total

    # ---------- HTML ----------
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
        for p in self.list():
            rs = p["RazonSocial"] or "(Sin cliente)"
            rows += f"""
            <tr>
              <td>{rs}</td>
              <td>{p["FechaPedido"] or ""}</td>
              <td class="text-center">
                <a class="btn btn-danger btn-sm"
                   href="/?d={b64_encode('odel/'+str(p['PedidoID']))}"
                   onclick="return confirm('¿Eliminar este pedido?');">Borrar</a>
              </td>
              <td class="text-center">
                <a class="btn btn-warning btn-sm"
                   href="/?d={b64_encode('oact/'+str(p['PedidoID']))}">Actualizar</a>
              </td>
              <td class="text-center">
                <a class="btn btn-info btn-sm"
                   href="/?d={b64_encode('odet/'+str(p['PedidoID']))}">Detalle</a>
              </td>
            </tr>
            """
        body = f"""
        <h2>Carritos de Compras (Pedidos)</h2>
        <div class="mb-3 text-end">
          <a class="btn btn-success" href="/?d={b64_encode('onew/0')}">Nuevo</a>
        </div>
        <div class="table-responsive">
          <table class="table table-striped table-hover align-middle">
            <thead class="table-dark">
              <tr>
                <th>Cliente</th><th>Fecha</th>
                <th colspan="3" class="text-center">Acciones</th>
              </tr>
            </thead>
            <tbody>{rows}</tbody>
          </table>
        </div>
        """
        return self._layout("Pedidos", body)

    def html_form_new(self, clientes) -> str:
        return self._layout("Nuevo Pedido", self._form_html("new", None, clientes))

    def html_form_update(self, pedido_id: int, clientes) -> str:
        return self._layout("Actualizar Pedido", self._form_html("update", self.get(pedido_id), clientes))

    def _form_html(self, modo: str, pedido, clientes):
        if modo == "new":
            op = "osave"
            pid = 0
            sel_id = 0
            fecha_txt = "Se genera automáticamente"
            titulo = "Formulario Carrito (Pedido)"
        else:
            op = "oupdate"
            pid = pedido["PedidoID"]
            sel_id = pedido["ClienteID"] or 0
            fecha_txt = pedido["FechaPedido"] or ""
            titulo = "Actualizar Pedido"

        opts = '<option value="">-- Seleccione Cliente --</option>'
        for c in clientes:
            selected = "selected" if int(c["ClienteID"]) == int(sel_id) else ""
            opts += f'<option value="{c["ClienteID"]}" {selected}>{c["RazonSocial"]}</option>'

        return f"""
        <div class="card shadow-sm">
          <div class="card-header bg-success text-white"><b>{titulo}</b></div>
          <div class="card-body">
            <form method="POST" action="/">
              <input type="hidden" name="op" value="{op}">
              <input type="hidden" name="PedidoID" value="{pid}">

              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Cliente</label>
                  <select class="form-select" name="ClienteID" required>
                    {opts}
                  </select>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Fecha Pedido</label>
                  <input class="form-control" value="{fecha_txt}" readonly>
                  <small class="text-muted">Se genera automáticamente con la hora actual.</small>
                </div>
              </div>

              <div class="mt-3 d-flex gap-2">
                <button class="btn btn-success" type="submit" name="Guardar">GUARDAR</button>
                <a class="btn btn-secondary" href="/?d={b64_encode('olist/0')}">REGRESAR</a>
              </div>
            </form>
          </div>
        </div>
        """

    def html_items(self, pedido_id: int, productos) -> str:
        items, total = self.items(pedido_id)

        # tabla items
        rows = ""
        if items:
            for it in items:
                rows += f"""
                <tr>
                  <td>{it["Descripcion"]}</td>
                  <td>${float(it["Precio"]):.2f}</td>
                  <td style="width:120px">
                    <input class="form-control" type="number" min="0"
                           name="qty[{it["ProductoID"]}]" value="{it["Cantidad"]}">
                  </td>
                  <td>${float(it["Subtotal"]):.2f}</td>
                  <td>
                    <a class="btn btn-sm btn-outline-danger"
                       href="/?d={b64_encode(f'orm/{pedido_id}/{it["ProductoID"]}')}">X</a>
                  </td>
                </tr>
                """
        else:
            rows = """<tr><td colspan="5">
                        <div class="alert alert-info m-0">Aún no agregas productos.</div>
                      </td></tr>"""

        # cards productos para agregar
        cards = ""
        for pr in productos:
            cards += f"""
            <div class="col-12">
              <div class="card shadow-sm">
                <div class="row g-0">
                  <div class="col-4">
                    <img src="/static/images/productos/{pr["Imagen"]}" class="img-fluid rounded-start"
                         style="height:90px;object-fit:cover" alt="">
                  </div>
                  <div class="col-8">
                    <div class="card-body p-2">
                      <div class="fw-bold">{pr["Descripcion"]}</div>
                      <div>${float(pr["Precio"]):.2f}</div>
                      <a class="btn btn-sm btn-success mt-1 w-100"
                         href="/?d={b64_encode(f'oadd/{pedido_id}/{pr["ProductoID"]}')}">Agregar</a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            """

        body = f"""
        <h4 class="mb-3">Elegir qué va a comprar (Pedido #{pedido_id})</h4>

        <div class="mb-3 d-flex gap-2 flex-wrap">
          <a class="btn btn-outline-secondary" href="/?d={b64_encode('olist/0')}">Volver a Pedidos</a>
          <a class="btn btn-outline-danger"
             href="/?d={b64_encode(f'oclear/{pedido_id}/0')}"
             onclick="return confirm('¿Vaciar productos del pedido?');">Vaciar</a>
          <a class="btn btn-info" href="/?d={b64_encode(f'odet/{pedido_id}') }">Ver Detalle</a>
        </div>

        <div class="row g-3">
          <div class="col-lg-7">
            <div class="card shadow-sm">
              <div class="card-header bg-dark text-white">Productos agregados</div>
              <div class="card-body">
                <form method="POST" action="/">
                  <input type="hidden" name="op" value="oitems_update">
                  <input type="hidden" name="PedidoID" value="{pedido_id}">

                  <div class="table-responsive">
                  <table class="table table-striped align-middle">
                    <thead>
                      <tr>
                        <th>Producto</th><th>Precio</th><th>Cantidad</th><th>Subtotal</th><th>Quitar</th>
                      </tr>
                    </thead>
                    <tbody>{rows}</tbody>
                    <tfoot>
                      <tr>
                        <th colspan="3" class="text-end">TOTAL</th>
                        <th colspan="2">${float(total):.2f}</th>
                      </tr>
                    </tfoot>
                  </table>
                  </div>

                  <button class="btn btn-primary" type="submit" name="Actualizar">Actualizar cantidades</button>
                </form>
              </div>
            </div>
          </div>

          <div class="col-lg-5">
            <div class="card shadow-sm">
              <div class="card-header bg-success text-white">Agregar productos</div>
              <div class="card-body">
                <div class="row g-2">{cards}</div>
              </div>
            </div>
          </div>
        </div>
        """
        return self._layout("Carrito", body)

    def html_detail(self, pedido_id: int) -> str:
        cab, det, total = self.detail(pedido_id)

        rows = ""
        for d in det:
            rows += f"""
            <tr>
              <td>{d["Descripcion"]}</td>
              <td>${float(d["Precio"]):.2f}</td>
              <td>{d["Cantidad"]}</td>
              <td>${float(d["Subtotal"]):.2f}</td>
            </tr>
            """

        body = f"""
        <div class="card shadow-sm">
          <div class="card-header bg-dark text-white"><b>Detalle del Pedido</b></div>
          <div class="card-body">
            <p><b>Cliente:</b> {cab["RazonSocial"] if cab and cab.get("RazonSocial") else ""}</p>
            <p><b>Fecha:</b> {cab["FechaPedido"] if cab and cab.get("FechaPedido") else ""}</p>

            <div class="table-responsive">
              <table class="table table-striped">
                <thead>
                  <tr><th>Producto</th><th>Precio</th><th>Cantidad</th><th>Subtotal</th></tr>
                </thead>
                <tbody>{rows}</tbody>
                <tfoot>
                  <tr>
                    <th colspan="3" class="text-end">TOTAL</th>
                    <th>${float(total):.2f}</th>
                  </tr>
                </tfoot>
              </table>
            </div>

            <a class="btn btn-outline-secondary" href="/?d={b64_encode('olist/0')}">Regresar</a>
            <a class="btn btn-success ms-2" href="/?d={b64_encode(f'oitems/{pedido_id}')}">Volver al carrito</a>
          </div>
        </div>
        """
        return self._layout("Detalle Pedido", body)
