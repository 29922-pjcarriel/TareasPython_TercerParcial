from flask import request

class Pedido:
    def __init__(self, cn):
        self.cn = cn

    # =========================
    # LISTADO DE PEDIDOS (sin botón "Productos" en la tabla)
    # =========================
    def get_list(self, U):
        cur = self.cn.cursor(dictionary=True)
        cur.execute("""
            SELECT p.PedidoID, p.FechaPedido, c.RazonSocial
            FROM Pedidos p
            LEFT JOIN Clientes c ON c.ClienteID=p.ClienteID
            ORDER BY p.PedidoID DESC
        """)
        rows = cur.fetchall()

        html = f"""
        <h2>Carritos de Compras (Pedidos)</h2>
        <div class="text-end mb-3">
          <a class="btn btn-success" href="{U('onew/0')}">Nuevo</a>
        </div>

        <div class="table-responsive">
        <table class="table table-striped table-hover align-middle">
          <thead class="table-dark">
            <tr>
              <th>Cliente</th>
              <th>Fecha</th>
              <th class="text-center">Borrar</th>
              <th class="text-center">Actualizar</th>
              <th class="text-center">Detalle</th>
            </tr>
          </thead>
          <tbody>
        """

        for r in rows:
            pid = int(r["PedidoID"])
            cliente = r.get("RazonSocial") or "-"
            fecha = r.get("FechaPedido") or ""
            html += f"""
            <tr>
              <td>{cliente}</td>
              <td>{fecha}</td>
              <td class="text-center">
                <a class="btn btn-danger btn-sm" href="{U(f"odel/{pid}")}" onclick="return confirm('¿Eliminar este pedido?');">Borrar</a>
              </td>
              <td class="text-center">
                <!-- En PHP: "Actualizar" entra a elegir productos -->
                <a class="btn btn-warning btn-sm" href="{U(f"oitems/{pid}")}">Actualizar</a>
              </td>
              <td class="text-center">
                <a class="btn btn-info btn-sm" href="{U(f"odet/{pid}")}">Detalle</a>
              </td>
            </tr>
            """

        html += "</tbody></table></div>"
        return html

    # =========================
    # NUEVO PEDIDO: solo cliente
    # =========================
    def get_form(self, U):
        cur = self.cn.cursor(dictionary=True)
        cur.execute("SELECT ClienteID, RazonSocial FROM Clientes ORDER BY RazonSocial")
        opts = "".join(
            f"<option value='{c['ClienteID']}'>{c['RazonSocial']}</option>"
            for c in cur.fetchall()
        )

        return f"""
        <h2>Nuevo Pedido</h2>
        <form method="POST">
          <input type="hidden" name="op" value="osave">
          <div class="mb-3">
            <label class="form-label">Cliente</label>
            <select class="form-select" name="ClienteID" required>
              {opts}
            </select>
          </div>
          <button class="btn btn-primary" type="submit" name="Guardar" value="1">Guardar</button>
          <a class="btn btn-secondary" href="{U("olist/0")}">Cancelar</a>
        </form>
        """

    # =========================
    # ELEGIR PRODUCTOS (pantalla tipo PHP, con fotos)
    # =========================
    def get_items(self, U, IMG, pid):
        pid = int(pid)

        # Lista productos
        cur = self.cn.cursor(dictionary=True)
        cur.execute("SELECT ProductoID, Descripcion, Precio, Imagen FROM Productos ORDER BY Descripcion")
        productos = cur.fetchall()

        # Items del pedido
        cur2 = self.cn.cursor(dictionary=True)
        cur2.execute("""
            SELECT i.PedidoItemID, i.ProductoID, i.Cantidad,
                   p.Descripcion, p.Precio, p.Imagen
            FROM PedidosItems i
            JOIN Productos p ON p.ProductoID=i.ProductoID
            WHERE i.PedidoID=%s
            ORDER BY i.PedidoItemID DESC
        """, (pid,))
        items = cur2.fetchall()

        # LEFT: tabla agregados
        rows = ""
        total = 0.0

        if not items:
            rows = """
            <tr>
              <td colspan="5">
                <div class="alert alert-info mb-0">Aún no agregas productos.</div>
              </td>
            </tr>
            """
        else:
            for it in items:
                precio = float(it["Precio"])
                qty = int(it["Cantidad"])
                subtotal = precio * qty
                total += subtotal
                img = it.get("Imagen") or "no-image.png"

                rows += f"""
                <tr>
                  <td>
                    <div class="d-flex gap-2 align-items-center">
                      <img src="{IMG(img)}" style="width:52px;height:52px;object-fit:cover;border-radius:10px;border:1px solid #ddd;">
                      <div>{it["Descripcion"]}</div>
                    </div>
                  </td>
                  <td>${precio:.2f}</td>
                  <td style="width:140px">
                    <input class="form-control" type="number" name="qty_{it["PedidoItemID"]}" value="{qty}" min="1">
                  </td>
                  <td class="fw-bold">${subtotal:.2f}</td>
                  <td class="text-center">
                    <a class="btn btn-danger btn-sm" href="{U(f"orm/{pid}/{it['ProductoID']}")}">Quitar</a>
                  </td>
                </tr>
                """

        # RIGHT: cards productos
        right_cards = ""
        for p in productos:
            img = p.get("Imagen") or "no-image.png"
            right_cards += f"""
            <div class="card mb-3 border-0 shadow-sm">
              <div class="card-body d-flex gap-3 align-items-center">
                <img src="{IMG(img)}" style="width:90px;height:70px;object-fit:cover;border-radius:10px;border:1px solid #ddd;">
                <div class="flex-grow-1">
                  <div class="h6 mb-1">{p["Descripcion"]}</div>
                  <div class="fw-bold">${float(p["Precio"]):.2f}</div>
                  <a class="btn btn-success w-100 mt-2" href="{U(f"oadd/{pid}/{p['ProductoID']}")}">Agregar</a>
                </div>
              </div>
            </div>
            """

        return f"""
        <h2>Elegir qué va a comprar (Pedido #{pid})</h2>

        <div class="mb-3 d-flex gap-2 flex-wrap">
          <a class="btn btn-outline-secondary" href="{U("olist/0")}">Volver a Pedidos</a>
          <a class="btn btn-outline-danger" href="{U(f"oclear/{pid}")}" onclick="return confirm('¿Vaciar carrito?');">Vaciar</a>
          <a class="btn btn-info text-white" href="{U(f"odet/{pid}")}">Ver Detalle</a>
        </div>

        <div class="row g-4">
          <div class="col-lg-7">
            <div class="card shadow-sm border-0">
              <div class="card-header bg-dark text-white"><b>Productos agregados</b></div>
              <div class="card-body">

                <form method="POST">
                  <input type="hidden" name="op" value="oitems_update">
                  <input type="hidden" name="PedidoID" value="{pid}">

                  <div class="table-responsive">
                    <table class="table table-striped align-middle mb-2">
                      <thead>
                        <tr>
                          <th>Producto</th>
                          <th>Precio</th>
                          <th>Cantidad</th>
                          <th>Subtotal</th>
                          <th class="text-center">Quitar</th>
                        </tr>
                      </thead>
                      <tbody>{rows}</tbody>
                    </table>
                  </div>

                  <div class="d-flex justify-content-end border-top pt-3">
                    <h5 class="mb-0">TOTAL&nbsp;&nbsp; <span class="fw-bold">${total:.2f}</span></h5>
                  </div>

                  <div class="mt-3 d-flex gap-2">
                    <button class="btn btn-primary" type="submit" name="Actualizar" value="1">Actualizar cantidades</button>
                    <a class="btn btn-success" href="{U(f"opay/{pid}")}">PAGAR</a>
                  </div>
                </form>

              </div>
            </div>
          </div>

          <div class="col-lg-5">
            <div class="card shadow-sm border-0">
              <div class="card-header text-white" style="background:#198754;"><b>Agregar productos</b></div>
              <div class="card-body">{right_cards}</div>
            </div>
          </div>
        </div>
        """

    # =========================
    # DETALLE REAL (arreglado)
    # =========================
    def get_detail(self, U, IMG, pid):
        pid = int(pid)

        cur = self.cn.cursor(dictionary=True)
        cur.execute("""
            SELECT p.PedidoID, p.FechaPedido, c.RazonSocial
            FROM Pedidos p
            LEFT JOIN Clientes c ON c.ClienteID=p.ClienteID
            WHERE p.PedidoID=%s
        """, (pid,))
        cab = cur.fetchone()
        if not cab:
            return "<div class='alert alert-warning'>Pedido no encontrado.</div>"

        cur2 = self.cn.cursor(dictionary=True)
        cur2.execute("""
            SELECT i.Cantidad, p.Descripcion, p.Precio, p.Imagen
            FROM PedidosItems i
            JOIN Productos p ON p.ProductoID=i.ProductoID
            WHERE i.PedidoID=%s
        """, (pid,))
        items = cur2.fetchall()

        rows = ""
        total = 0.0

        if not items:
            rows = "<tr><td colspan='5'><div class='alert alert-info mb-0'>Pedido sin productos.</div></td></tr>"
        else:
            for it in items:
                precio = float(it["Precio"])
                qty = int(it["Cantidad"])
                sub = precio * qty
                total += sub
                img = it.get("Imagen") or "no-image.png"
                rows += f"""
                <tr>
                  <td>
                    <div class="d-flex gap-2 align-items-center">
                      <img src="{IMG(img)}" style="width:52px;height:52px;object-fit:cover;border-radius:10px;border:1px solid #ddd;">
                      <div>{it["Descripcion"]}</div>
                    </div>
                  </td>
                  <td>${precio:.2f}</td>
                  <td>{qty}</td>
                  <td>${sub:.2f}</td>
                </tr>
                """

        return f"""
        <h2>Detalle del Pedido #{pid}</h2>

        <div class="card p-3 mb-3">
          <p class="mb-1"><b>Cliente:</b> {cab.get("RazonSocial") or "-"}</p>
          <p class="mb-0"><b>Fecha:</b> {cab.get("FechaPedido") or ""}</p>
        </div>

        <div class="table-responsive">
          <table class="table table-striped align-middle">
            <thead class="table-dark">
              <tr><th>Producto</th><th>Precio</th><th>Cantidad</th><th>Subtotal</th></tr>
            </thead>
            <tbody>{rows}</tbody>
          </table>
        </div>

        <h4 class="text-end">TOTAL ${total:.2f}</h4>

        <div class="mt-3 d-flex gap-2">
          <a class="btn btn-primary" href="{U(f"oitems/{pid}")}">Actualizar (Productos)</a>
          <a class="btn btn-secondary" href="{U("olist/0")}">Volver</a>
        </div>
        """

    # =========================
    # OPERACIONES
    # =========================
    def save_pedido(self):
        cid = int(request.form["ClienteID"])
        cur = self.cn.cursor()
        cur.execute("INSERT INTO Pedidos (ClienteID, FechaPedido) VALUES (%s, NOW())", (cid,))
        return cur.lastrowid

    def delete_pedido(self, pid):
        cur = self.cn.cursor()
        cur.execute("DELETE FROM PedidosItems WHERE PedidoID=%s", (pid,))
        cur.execute("DELETE FROM Pedidos WHERE PedidoID=%s", (pid,))

    def add_item(self, pid, prod):
        pid = int(pid); prod = int(prod)
        cur = self.cn.cursor(dictionary=True)
        cur.execute("SELECT PedidoItemID, Cantidad FROM PedidosItems WHERE PedidoID=%s AND ProductoID=%s", (pid, prod))
        r = cur.fetchone()

        cur2 = self.cn.cursor()
        if r:
            cur2.execute("UPDATE PedidosItems SET Cantidad=Cantidad+1 WHERE PedidoItemID=%s", (r["PedidoItemID"],))
        else:
            cur2.execute("INSERT INTO PedidosItems (PedidoID, ProductoID, Cantidad) VALUES (%s,%s,1)", (pid, prod))

    def rm_item(self, pid, prod):
        pid = int(pid); prod = int(prod)
        cur = self.cn.cursor()
        cur.execute("DELETE FROM PedidosItems WHERE PedidoID=%s AND ProductoID=%s", (pid, prod))

    def clear_items(self, pid):
        pid = int(pid)
        cur = self.cn.cursor()
        cur.execute("DELETE FROM PedidosItems WHERE PedidoID=%s", (pid,))

    def update_qty(self):
        pid = int(request.form["PedidoID"])
        cur = self.cn.cursor(dictionary=True)
        cur.execute("SELECT PedidoItemID FROM PedidosItems WHERE PedidoID=%s", (pid,))
        items = cur.fetchall()

        cur2 = self.cn.cursor()
        for it in items:
            iid = int(it["PedidoItemID"])
            qty = int(request.form.get(f"qty_{iid}", "1"))
            if qty < 1:
                qty = 1
            cur2.execute("UPDATE PedidosItems SET Cantidad=%s WHERE PedidoItemID=%s", (qty, iid))

        return pid

    def pay(self, U, pid):
        pid = int(pid)
        # (Opcional) marcar estado si tu tabla lo tiene; si no, no rompe.
        try:
            cur = self.cn.cursor()
            cur.execute("UPDATE Pedidos SET Estado='PAGADO' WHERE PedidoID=%s", (pid,))
        except Exception:
            pass

        return f"""
        <div class="alert alert-success">✅ Pedido pagado correctamente.</div>
        <script>
          setTimeout(function() {{
            window.location = "{U("olist/0")}";
          }}, 1200);
        </script>
        """
