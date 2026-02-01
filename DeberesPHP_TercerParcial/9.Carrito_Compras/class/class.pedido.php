<?php
class pedido{

  private $con;

  function __construct($cn){
    $this->con = $cn;
  }

  /* =====================================================
     LISTAR PEDIDOS (SIN ID)
     ===================================================== */
  public function get_list_pedidos(){

    $d_new = base64_encode("onew/0");

    $html = '
    <h2>Carritos de Compras (Pedidos)</h2>

    <div class="mb-3 text-end">
      <a class="btn btn-success" href="index.php?d='.$d_new.'">Nuevo</a>
    </div>

    <div class="table-responsive">
    <table class="table table-striped table-hover align-middle">
      <thead class="table-dark">
        <tr>
          <th>Cliente</th>
          <th>Fecha</th>
          <th colspan="3" class="text-center">Acciones</th>
        </tr>
      </thead>
      <tbody>';

    $sql = "SELECT p.PedidoID, p.FechaPedido, c.RazonSocial
            FROM Pedidos p
            LEFT JOIN Clientes c ON c.ClienteID=p.ClienteID
            ORDER BY p.PedidoID DESC;";

    $res = $this->con->query($sql);

    while($row = $res->fetch_assoc()){
      $id = (int)$row["PedidoID"];
      $cliente = $row["RazonSocial"];
      if($cliente == NULL || $cliente == "") $cliente = "(Sin cliente)";

      $html .= '
      <tr>
        <td>'.$cliente.'</td>
        <td>'.$row["FechaPedido"].'</td>

        <td class="text-center">
          <a class="btn btn-danger btn-sm"
             href="index.php?d='.base64_encode("odel/".$id).'"
             onclick="return confirm(\'¿Eliminar este pedido?\');">
             Borrar
          </a>
        </td>

        <td class="text-center">
          <a class="btn btn-warning btn-sm"
             href="index.php?d='.base64_encode("oact/".$id).'">
             Actualizar
          </a>
        </td>

        <td class="text-center">
          <a class="btn btn-info btn-sm"
             href="index.php?d='.base64_encode("odet/".$id).'">
             Detalle
          </a>
        </td>
      </tr>';
    }

    $html .= '</tbody></table></div>';
    return $html;
  }

  /* =====================================================
     FORM PEDIDO: Nuevo / Actualizar
     ✅ Fecha se muestra pero NO se envía (sin name)
     ✅ Hora siempre es la del servidor al cargar
     ===================================================== */
  public function get_form_pedido($clienteObj, $id=NULL){

    if($id == NULL){
      $PedidoID = 0;
      $ClienteID = NULL;
      $op = "osave";
      $titulo = "Formulario Carrito (Pedido)";
      $fechaMostrar = date("Y-m-d H:i:s"); // hora actual
    }else{
      $id = (int)$id;
      $sql = "SELECT * FROM Pedidos WHERE PedidoID=$id;";
      $res = $this->con->query($sql);

      if(!$res || $res->num_rows==0){
        return $this->message_error("Pedido no encontrado");
      }
      $row = $res->fetch_assoc();

      $PedidoID = (int)$row["PedidoID"];
      $ClienteID = $row["ClienteID"];
      $op = "oupdate";
      $titulo = "Actualizar Pedido";
      $fechaMostrar = $row["FechaPedido"]; // solo mostrar
    }

    $html = '
    <div class="card shadow-sm">
      <div class="card-header bg-success text-white"><b>'.$titulo.'</b></div>
      <div class="card-body">

        <form method="POST" action="index.php">
          <input type="hidden" name="PedidoID" value="'.$PedidoID.'">
          <input type="hidden" name="op" value="'.$op.'">

          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label">Cliente</label>
              '.$clienteObj->combo_clientes($ClienteID).'
            </div>

            <div class="col-md-6">
              <label class="form-label">Fecha Pedido</label>
              <!-- ✅ SOLO SE MUESTRA: SIN name y readonly -->
              <input class="form-control" type="text" value="'.$fechaMostrar.'" readonly>
              <small class="text-muted">Se genera automáticamente con la hora actual.</small>
            </div>
          </div>

          <div class="mt-3 d-flex gap-2">
            <button class="btn btn-success" type="submit" name="Guardar">GUARDAR</button>
            <a class="btn btn-secondary" href="index.php?d='.base64_encode("olist/0").'">REGRESAR</a>
          </div>

        </form>

      </div>
    </div>';

    return $html;
  }

  /* =====================================================
     GUARDAR PEDIDO
     ✅ Fecha real siempre del servidor (NO del input)
     ===================================================== */
  public function save_pedido_redirect_to_items(){

    $clienteId = (int)($_POST["ClienteID"] ?? 0);
    $fecha = date("Y-m-d H:i:s"); // ✅ hora real servidor

    if($clienteId <= 0){
      echo $this->message_error("Seleccione un cliente");
      return;
    }

    $sql = "INSERT INTO Pedidos(ClienteID, FechaPedido)
            VALUES ($clienteId,'$fecha');";

    if($this->con->query($sql)){
      $nuevoId = (int)$this->con->insert_id;
      header("Location: index.php?d=".base64_encode("oitems/".$nuevoId));
      exit;
    }

    echo $this->message_error("No se pudo crear el pedido");
  }

  /* =====================================================
     UPDATE Pedido
     (si quieres NO cambiar fecha, aquí no la tocamos)
     ===================================================== */
  public function update_pedido(){

    $id = (int)($_POST["PedidoID"] ?? 0);
    $clienteId = (int)($_POST["ClienteID"] ?? 0);

    if($id <= 0){
      echo $this->message_error("Pedido inválido");
      return;
    }
    if($clienteId <= 0){
      echo $this->message_error("Seleccione un cliente");
      return;
    }

    // ✅ NO CAMBIAMOS FechaPedido (queda intacta)
    $sql = "UPDATE Pedidos
            SET ClienteID=$clienteId
            WHERE PedidoID=$id;";

    if($this->con->query($sql)){
      echo $this->message_ok("Pedido actualizado");
    }else{
      echo $this->message_error("No se pudo actualizar el pedido");
    }
  }

  /* =====================================================
     oitems: elegir productos + PAGAR
     ===================================================== */
  public function get_items_form($pedidoId){

    $pedidoId = (int)$pedidoId;

    $sql = "SELECT i.ProductoID, i.Cantidad, p.Descripcion, p.Precio, p.Imagen
            FROM PedidosItems i, Productos p
            WHERE i.PedidoID=$pedidoId AND i.ProductoID=p.ProductoID
            ORDER BY p.ProductoID DESC;";

    $res = $this->con->query($sql);
    $total = 0;

    $d_pay = base64_encode("opay/".$pedidoId);

    $html = '
    <h4 class="mb-3">Elegir qué va a comprar (Pedido #'.$pedidoId.')</h4>

    <div class="mb-3 d-flex gap-2 flex-wrap">
      <a class="btn btn-outline-secondary" href="index.php?d='.base64_encode("olist/0").'">Volver a Pedidos</a>
      <a class="btn btn-outline-danger"
         href="index.php?d='.base64_encode("oclear/".$pedidoId."/0").'"
         onclick="return confirm(\'¿Vaciar productos del pedido?\');">
         Vaciar
      </a>
      <a class="btn btn-info" href="index.php?d='.base64_encode("odet/".$pedidoId).'">Ver Detalle</a>
    </div>

    <div class="row g-3">
      <div class="col-lg-7">
        <div class="card shadow-sm">
          <div class="card-header bg-dark text-white">Productos agregados</div>
          <div class="card-body">

            <form method="POST" action="index.php">
              <input type="hidden" name="op" value="oitems_update">
              <input type="hidden" name="PedidoID" value="'.$pedidoId.'">

              <div class="table-responsive">
              <table class="table table-striped align-middle">
                <thead>
                  <tr>
                    <th>Producto</th>
                    <th>Precio</th>
                    <th style="width:120px;">Cantidad</th>
                    <th>Subtotal</th>
                    <th>Quitar</th>
                  </tr>
                </thead>
                <tbody>';

    if($res && $res->num_rows > 0){
      while($row = $res->fetch_assoc()){
        $prodId = (int)$row["ProductoID"];
        $precio = (float)$row["Precio"];
        $cant = (int)$row["Cantidad"];
        $sub = $precio * $cant;
        $total += $sub;

        $html .= '
        <tr>
          <td>'.$row["Descripcion"].'</td>
          <td>$'.number_format($precio,2).'</td>
          <td>
            <input class="form-control" type="number" min="0"
                   name="qty['.$prodId.']" value="'.$cant.'">
          </td>
          <td>$'.number_format($sub,2).'</td>
          <td>
            <a class="btn btn-sm btn-outline-danger"
               href="index.php?d='.base64_encode("orm/".$pedidoId."/".$prodId).'">X</a>
          </td>
        </tr>';
      }
    }else{
      $html .= '<tr><td colspan="5"><div class="alert alert-info m-0">Aún no agregas productos.</div></td></tr>';
    }

    $html .= '
                </tbody>
                <tfoot>
                  <tr>
                    <th colspan="3" class="text-end">TOTAL</th>
                    <th colspan="2">$'.number_format($total,2).'</th>
                  </tr>
                </tfoot>
              </table>
              </div>

              <button class="btn btn-primary" type="submit" name="Actualizar">Actualizar cantidades</button>

              <a class="btn btn-success ms-2"
                 href="index.php?d='.$d_pay.'"
                 onclick="return confirm(\'¿Desea confirmar el pago del pedido?\');">
                 PAGAR
              </a>

            </form>

          </div>
        </div>
      </div>

      <div class="col-lg-5">
        <div class="card shadow-sm">
          <div class="card-header bg-success text-white">Agregar productos</div>
          <div class="card-body">
            '.$this->render_product_picker($pedidoId).'
          </div>
        </div>
      </div>
    </div>';

    return $html;
  }

  private function render_product_picker($pedidoId){

    $pedidoId = (int)$pedidoId;

    $sql = "SELECT * FROM Productos ORDER BY ProductoID DESC;";
    $res = $this->con->query($sql);

    $html = '<div class="row g-2">';

    while($row = $res->fetch_assoc()){
      $prodId = (int)$row["ProductoID"];
      $d_add = base64_encode("oadd/".$pedidoId."/".$prodId);

      $img = $row["Imagen"];
      if($img == "" || $img == NULL) $img = "no-image.png";

      $html .= '
      <div class="col-12">
        <div class="card shadow-sm">
          <div class="row g-0">
            <div class="col-4">
              <img src="images/productos/'.$img.'" class="img-fluid rounded-start"
                   style="height:90px;object-fit:cover" alt="">
            </div>
            <div class="col-8">
              <div class="card-body p-2">
                <div class="fw-bold">'.$row["Descripcion"].'</div>
                <div>$'.number_format((float)$row["Precio"],2).'</div>
                <a class="btn btn-sm btn-success mt-1 w-100" href="index.php?d='.$d_add.'">Agregar</a>
              </div>
            </div>
          </div>
        </div>
      </div>';
    }

    $html .= '</div>';
    return $html;
  }

  public function pedido_add_item($pedidoId, $prodId){
    $pedidoId = (int)$pedidoId;
    $prodId   = (int)$prodId;

    $sql = "SELECT Cantidad FROM PedidosItems WHERE PedidoID=$pedidoId AND ProductoID=$prodId;";
    $res = $this->con->query($sql);

    if($res && $res->num_rows > 0){
      $row = $res->fetch_assoc();
      $cant = (int)$row["Cantidad"] + 1;
      $this->con->query("UPDATE PedidosItems SET Cantidad=$cant WHERE PedidoID=$pedidoId AND ProductoID=$prodId;");
    }else{
      $this->con->query("INSERT INTO PedidosItems(PedidoID,ProductoID,Cantidad) VALUES ($pedidoId,$prodId,1);");
    }

    header("Location: index.php?d=".base64_encode("oitems/".$pedidoId));
    exit;
  }

  public function pedido_rm_item($pedidoId, $prodId){
    $pedidoId = (int)$pedidoId;
    $prodId   = (int)$prodId;

    $this->con->query("DELETE FROM PedidosItems WHERE PedidoID=$pedidoId AND ProductoID=$prodId;");

    header("Location: index.php?d=".base64_encode("oitems/".$pedidoId));
    exit;
  }

  public function pedido_clear_items($pedidoId){
    $pedidoId = (int)$pedidoId;
    $this->con->query("DELETE FROM PedidosItems WHERE PedidoID=$pedidoId;");
    header("Location: index.php?d=".base64_encode("oitems/".$pedidoId));
    exit;
  }

  public function pedido_update_qty(){
    $pedidoId = (int)($_POST["PedidoID"] ?? 0);

    if(isset($_POST["qty"])){
      foreach($_POST["qty"] as $prodId => $qty){
        $prodId = (int)$prodId;
        $qty    = (int)$qty;

        if($qty <= 0){
          $this->con->query("DELETE FROM PedidosItems WHERE PedidoID=$pedidoId AND ProductoID=$prodId;");
        }else{
          $this->con->query("UPDATE PedidosItems SET Cantidad=$qty WHERE PedidoID=$pedidoId AND ProductoID=$prodId;");
        }
      }
    }

    header("Location: index.php?d=".base64_encode("oitems/".$pedidoId));
    exit;
  }

  /* =====================================================
     PAGAR: mensaje y regresar a pedidos
     ===================================================== */
  public function pagar_pedido($pedidoId){
    $pedidoId = (int)$pedidoId;

    $sql = "SELECT COUNT(*) AS total FROM PedidosItems WHERE PedidoID=$pedidoId;";
    $res = $this->con->query($sql);
    $row = $res ? $res->fetch_assoc() : ["total"=>0];

    if((int)$row["total"] <= 0){
      echo '<div class="alert alert-warning">No se puede pagar un pedido sin productos.</div>
            <a class="btn btn-secondary" href="index.php?d='.base64_encode("oitems/".$pedidoId).'">Volver</a>';
      return;
    }

    // Si no existe Estado, no rompe
    @ $this->con->query("UPDATE Pedidos SET Estado='PAGADO' WHERE PedidoID=$pedidoId;");

    echo '
      <div class="alert alert-success">✅ Pedido pagado exitosamente</div>
      <script>
        setTimeout(function(){
          window.location = "index.php?d='.base64_encode("olist/0").'";
        }, 1200);
      </script>
    ';
  }

  public function get_detail_pedido($id){
    $id = (int)$id;

    $sqlCab = "SELECT p.FechaPedido, c.RazonSocial
               FROM Pedidos p
               LEFT JOIN Clientes c ON c.ClienteID=p.ClienteID
               WHERE p.PedidoID=$id;";
    $resCab = $this->con->query($sqlCab);

    if(!$resCab || $resCab->num_rows==0){
      return $this->message_error("Pedido no encontrado");
    }
    $cab = $resCab->fetch_assoc();

    $sqlDet = "SELECT i.Cantidad, pr.Descripcion, pr.Precio
               FROM PedidosItems i, Productos pr
               WHERE i.PedidoID=$id AND i.ProductoID=pr.ProductoID;";
    $resDet = $this->con->query($sqlDet);

    $total = 0;

    $html = '
    <div class="card shadow-sm">
      <div class="card-header bg-dark text-white"><b>Detalle del Pedido</b></div>
      <div class="card-body">
        <p><b>Cliente:</b> '.$cab["RazonSocial"].'</p>
        <p><b>Fecha:</b> '.$cab["FechaPedido"].'</p>

        <div class="table-responsive">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Producto</th>
              <th>Precio</th>
              <th>Cantidad</th>
              <th>Subtotal</th>
            </tr>
          </thead>
          <tbody>';

    while($row = $resDet->fetch_assoc()){
      $sub = ((float)$row["Precio"]) * ((int)$row["Cantidad"]);
      $total += $sub;

      $html .= '
      <tr>
        <td>'.$row["Descripcion"].'</td>
        <td>$'.number_format((float)$row["Precio"],2).'</td>
        <td>'.$row["Cantidad"].'</td>
        <td>$'.number_format($sub,2).'</td>
      </tr>';
    }

    $html .= '
          </tbody>
          <tfoot>
            <tr>
              <th colspan="3" class="text-end">TOTAL</th>
              <th>$'.number_format($total,2).'</th>
            </tr>
          </tfoot>
        </table>
        </div>

        <div class="d-flex gap-2">
          <a class="btn btn-outline-secondary" href="index.php?d='.base64_encode("olist/0").'">Volver</a>
          <a class="btn btn-success" href="index.php?d='.base64_encode("oitems/".$id).'">Editar productos</a>
        </div>

      </div>
    </div>';

    return $html;
  }

  public function delete_pedido($id){
    $id = (int)$id;

    $this->con->query("DELETE FROM PedidosItems WHERE PedidoID=$id;");
    $sql = "DELETE FROM Pedidos WHERE PedidoID=$id;";

    if($this->con->query($sql)){
      echo $this->message_ok("Pedido eliminado");
    }else{
      echo $this->message_error("No se pudo eliminar el pedido");
    }
  }

  public function message_ok($msg){
    return '<div class="alert alert-success">'.$msg.'</div>';
  }

  public function message_error($msg){
    return '<div class="alert alert-danger">'.$msg.'</div>';
  }
}
?>
