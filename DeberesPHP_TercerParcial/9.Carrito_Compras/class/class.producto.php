<?php
class producto{
  private $ProductoID;
  private $Descripcion;
  private $Precio;
  private $Imagen;
  private $Detalles;
  private $con;

  function __construct($cn){
    $this->con = $cn;
  }

  public function save_producto(){
    $this->Descripcion = $_POST['Descripcion'];
    $this->Precio = $_POST['Precio'];
    $this->Detalles = $_POST['Detalles'];

    $this->Imagen = $_FILES['Imagen']['name'];
    if($this->Imagen == NULL || $this->Imagen == ""){
      $this->Imagen = "no-image.png";
    }else{
      $path = "images/productos/" . $this->Imagen;
      if(!move_uploaded_file($_FILES['Imagen']['tmp_name'], $path)){
        echo $this->_message_error("Cargar la imagen");
        exit;
      }
    }

    $sql = "INSERT INTO Productos VALUES(NULL,
              '$this->Descripcion',
              $this->Precio,
              '$this->Imagen',
              '$this->Detalles');";

    if($this->con->query($sql)){
      echo $this->_message_ok("guardó");
    }else{
      echo $this->_message_error("guardar");
    }
  }

  public function update_producto(){
    $this->ProductoID = (int)$_POST['ProductoID'];
    $this->Descripcion = $_POST['Descripcion'];
    $this->Precio = $_POST['Precio'];
    $this->Detalles = $_POST['Detalles'];

    $imgActual = $_POST['ImagenActual'];
    $this->Imagen = $imgActual;

    if(isset($_FILES['Imagen']) && $_FILES['Imagen']['name'] != ""){
      $this->Imagen = $_FILES['Imagen']['name'];
      $path = "images/productos/" . $this->Imagen;

      if(!move_uploaded_file($_FILES['Imagen']['tmp_name'], $path)){
        echo $this->_message_error("Cargar la imagen");
        exit;
      }
    }

    $sql = "UPDATE Productos SET
              Descripcion='$this->Descripcion',
              Precio=$this->Precio,
              Imagen='$this->Imagen',
              Detalles='$this->Detalles'
            WHERE ProductoID=$this->ProductoID;";

    if($this->con->query($sql)){
      echo $this->_message_ok("modificó");
    }else{
      echo $this->_message_error("al modificar");
    }
  }

  public function delete_producto($id){
    $sql = "DELETE FROM Productos WHERE ProductoID=$id;";
    if($this->con->query($sql)){
      echo $this->_message_ok("ELIMINÓ");
    }else{
      echo $this->_message_error("eliminar");
    }
  }

  public function get_form($id=NULL){

    if($id == NULL){
      $this->Descripcion = NULL;
      $this->Precio = NULL;
      $this->Imagen = NULL;
      $this->Detalles = NULL;

      $op = "pnew";
      $titulo = "Nuevo Producto";
      $flag = NULL;
      $ProductoID = 0;

    }else{
      $sql = "SELECT * FROM Productos WHERE ProductoID=$id;";
      $res = $this->con->query($sql);
      $row = $res->fetch_assoc();

      $num = $res->num_rows;
      if($num==0){
        $mensaje = "tratar de actualizar el producto con id= ".$id;
        echo $this->_message_error($mensaje);
      }else{
        $ProductoID = $row['ProductoID'];
        $this->Descripcion = $row['Descripcion'];
        $this->Precio = $row['Precio'];
        $this->Imagen = $row['Imagen'];
        $this->Detalles = $row['Detalles'];

        $op = "pupdate";
        $titulo = "Actualizar Producto";
        $flag = NULL;
      }
    }

    $html = '
    <div class="card shadow-sm">
      <div class="card-header bg-dark text-white"><b>'.$titulo.'</b></div>
      <div class="card-body">
        <form method="POST" action="index.php" enctype="multipart/form-data">
          <input type="hidden" name="ProductoID" value="'.$ProductoID.'">
          <input type="hidden" name="op" value="'.$op.'">
          <input type="hidden" name="ImagenActual" value="'.$this->Imagen.'">

          <div class="mb-3">
            <label class="form-label">Descripción</label>
            <input class="form-control" type="text" name="Descripcion" value="'.$this->Descripcion.'" required>
          </div>

          <div class="mb-3">
            <label class="form-label">Precio</label>
            <input class="form-control" type="text" name="Precio" value="'.$this->Precio.'" required>
          </div>

          <div class="mb-3">
            <label class="form-label">Detalles</label>
            <input class="form-control" type="text" name="Detalles" value="'.$this->Detalles.'" required>
          </div>

          <div class="mb-3">
            <label class="form-label">Imagen</label>
            <input class="form-control" type="file" name="Imagen" '.$flag.'>
            <div class="mt-2">
              <img class="img-thumbnail" style="width:200px" src="images/productos/'.$this->Imagen.'" alt="">
            </div>
          </div>

          <div class="d-flex gap-2">
            <input class="btn btn-primary" type="submit" name="Guardar" value="GUARDAR">
            <a class="btn btn-outline-secondary" href="index.php?d='.base64_encode("plist/0").'">Regresar</a>
          </div>

        </form>
      </div>
    </div>';

    return $html;
  }

  public function get_list(){
    $d_new = base64_encode("pnew/0");
    $html = '
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h4 class="m-0">Lista de Productos</h4>
      <a class="btn btn-success" href="index.php?d='.$d_new.'">Nuevo</a>
    </div>

    <div class="card shadow-sm">
    <div class="table-responsive">
    <table class="table table-striped table-hover align-middle mb-0">
      <thead class="table-dark">
        <tr>
          <th>Imagen</th>
          <th>Descripción</th>
          <th>Precio</th>
          <th>Detalles</th>
          <th colspan="3">Acciones</th>
        </tr>
      </thead>
      <tbody>';

    $sql = "SELECT * FROM Productos ORDER BY ProductoID DESC;";
    $res = $this->con->query($sql);

    while($row = $res->fetch_assoc()){
      $d_del = base64_encode("pdel/".$row['ProductoID']);
      $d_act = base64_encode("pact/".$row['ProductoID']);
      $d_det = base64_encode("pdet/".$row['ProductoID']);

      $html .= '
      <tr>
        <td><img class="img-thumbnail" style="width:90px" src="images/productos/'.$row['Imagen'].'" alt=""></td>
        <td>'.$row['Descripcion'].'</td>
        <td>$'.$row['Precio'].'</td>
        <td>'.$row['Detalles'].'</td>
        <td><a class="btn btn-sm btn-outline-danger" href="index.php?d='.$d_del.'">Borrar</a></td>
        <td><a class="btn btn-sm btn-outline-warning" href="index.php?d='.$d_act.'">Actualizar</a></td>
        <td><a class="btn btn-sm btn-outline-info" href="index.php?d='.$d_det.'">Detalle</a></td>
      </tr>';
    }

    $html .= '
      </tbody>
    </table>
    </div></div>';

    return $html;
  }

  public function get_detail_producto($id){
    $sql = "SELECT * FROM Productos WHERE ProductoID=$id;";
    $res = $this->con->query($sql);
    $row = $res->fetch_assoc();

    $num = $res->num_rows;
    if($num==0){
      $mensaje = "tratar de ver detalle del producto con id= ".$id;
      echo $this->_message_error($mensaje);
    }else{
      $html = '
      <div class="card shadow-sm">
        <div class="card-header bg-dark text-white"><b>Detalle Producto</b></div>
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-4">
              <img class="img-fluid img-thumbnail" src="images/productos/'.$row['Imagen'].'" alt="">
            </div>
            <div class="col-md-8">
              <p><b>Descripción:</b> '.$row['Descripcion'].'</p>
              <p><b>Precio:</b> $'.$row['Precio'].'</p>
              <p><b>Detalles:</b> '.$row['Detalles'].'</p>
              <a class="btn btn-outline-secondary" href="index.php?d='.base64_encode("plist/0").'">Regresar</a>
            </div>
          </div>
        </div>
      </div>';
      return $html;
    }
  }

  public function get_shop(){
    $html = '
    <h4 class="mb-3">Tienda</h4>
    <div class="row g-3">';

    $sql = "SELECT * FROM Productos ORDER BY ProductoID DESC;";
    $res = $this->con->query($sql);

    while($row = $res->fetch_assoc()){
      $d_add = base64_encode("add/".$row['ProductoID']);

      $html .= '
      <div class="col-md-4">
        <div class="card shadow-sm h-100">
          <img src="images/productos/'.$row['Imagen'].'" class="card-img-top" style="height:200px;object-fit:cover" alt="">
          <div class="card-body">
            <h5 class="card-title">'.$row['Descripcion'].'</h5>
            <p class="card-text">'.$row['Detalles'].'</p>
            <p class="fw-bold">$'.$row['Precio'].'</p>
          </div>
          <div class="card-footer bg-white">
            <a class="btn btn-success w-100" href="index.php?d='.$d_add.'">Agregar al carrito</a>
          </div>
        </div>
      </div>';
    }

    $html .= '</div>';
    return $html;
  }

  public function get_producto($id){
    $sql = "SELECT * FROM Productos WHERE ProductoID=$id;";
    $res = $this->con->query($sql);
    if($res->num_rows > 0) return $res->fetch_assoc();
    return NULL;
  }

  private function _message_error($tipo){
    $html = '
    <div class="alert alert-danger">
      Error al '.$tipo.'. Favor contactar a ....................
      <div class="mt-2"><a class="btn btn-sm btn-dark" href="index.php">Regresar</a></div>
    </div>';
    return $html;
  }

  private function _message_ok($tipo){
    $html = '
    <div class="alert alert-success">
      El registro se '.$tipo.' correctamente
      <div class="mt-2"><a class="btn btn-sm btn-dark" href="index.php">Regresar</a></div>
    </div>';
    return $html;
  }
}
?>
