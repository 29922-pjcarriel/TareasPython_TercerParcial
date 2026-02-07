<?php
class marca{

  private $id;
  private $descripcion;
  private $pais;
  private $direccion;
  private $foto;
  private $con;

  function __construct($cn){
    $this->con = $cn;
  }

  // ========================= GUARDAR =========================
  public function save_marca(){

    $this->descripcion = $_POST['descripcion'];
    $this->pais        = $_POST['pais'];
    $this->direccion   = $_POST['direccion'];

    $this->foto = $_FILES['foto']['name'];
    $path = "./imagenes/" . $this->foto;

    if(!move_uploaded_file($_FILES['foto']['tmp_name'], $path)){
      return $this->_message_error("cargar la imagen");
    }

    $sql = "INSERT INTO marca VALUES(
              NULL,
              '$this->descripcion',
              '$this->pais',
              '$this->direccion',
              '$this->foto'
            );";

    if($this->con->query($sql)){
      return $this->_message_ok("GUARDÓ");
    }else{
      return $this->_message_error("guardar<br><br>".$this->con->error);
    }
  }

  // ========================= ACTUALIZAR =========================
  public function update_marca(){

    $this->id          = $_POST['id'];
    $this->descripcion = $_POST['descripcion'];
    $this->pais        = $_POST['pais'];
    $this->direccion   = $_POST['direccion'];

    // Si no sube nueva foto, conserva la anterior
    $foto_nueva = $_FILES['foto']['name'];
    if($foto_nueva != ""){
      $this->foto = $foto_nueva;
      $path = "../imagenes/" . $this->foto;

      if(!move_uploaded_file($_FILES['foto']['tmp_name'], $path)){
        return $this->_message_error("cargar la imagen");
      }

      $sql = "UPDATE marca SET
                descripcion='$this->descripcion',
                pais='$this->pais',
                direccion='$this->direccion',
                foto='$this->foto'
              WHERE id=$this->id;";
    }else{
      $sql = "UPDATE marca SET
                descripcion='$this->descripcion',
                pais='$this->pais',
                direccion='$this->direccion'
              WHERE id=$this->id;";
    }

    if($this->con->query($sql)){
      return $this->_message_ok("MODIFICÓ");
    }else{
      return $this->_message_error("modificar<br><br>".$this->con->error);
    }
  }

  // ========================= FORMULARIO =========================
  public function get_form($id=NULL){

    if($id == NULL){
      $this->descripcion = NULL;
      $this->pais = NULL;
      $this->direccion = NULL;
      $this->foto = NULL;

      $op = "new";
      $flag = NULL; // permite cargar foto
    }else{

      $sql = "SELECT * FROM marca WHERE id=$id;";
      $res = $this->con->query($sql);

      if(!$res || $res->num_rows==0){
        return $this->_message_error("consultar marca<br><br>".$this->con->error);
      }

      $row = $res->fetch_assoc();

      $this->descripcion = $row['descripcion'];
      $this->pais = $row['pais'];
      $this->direccion = $row['direccion'];
      $this->foto = $row['foto'];

      $op = "update";
      $flag = NULL; // en update dejamos opcional subir nueva foto
    }

    $html = '
    <div class="card shadow-sm">
      <div class="card-header bg-dark text-white fw-bold">DATOS MARCA</div>
      <div class="card-body">

        <form method="POST" action="index.php?mod=marca" enctype="multipart/form-data">
          <input type="hidden" name="id" value="'.$id.'">
          <input type="hidden" name="op" value="'.$op.'">

          <div class="row g-3">

            <div class="col-md-6">
              <label class="form-label fw-semibold">Descripción</label>
              <input class="form-control" type="text" name="descripcion" value="'.$this->descripcion.'" required>
            </div>

            <div class="col-md-6">
              <label class="form-label fw-semibold">País</label>
              <input class="form-control" type="text" name="pais" value="'.$this->pais.'" required>
            </div>

            <div class="col-12">
              <label class="form-label fw-semibold">Dirección</label>
              <input class="form-control" type="text" name="direccion" value="'.$this->direccion.'" required>
            </div>

            <div class="col-12">
              <label class="form-label fw-semibold">Foto</label>
              <input class="form-control" type="file" name="foto" '.$flag.'>
              <div class="form-text">En actualizar, la foto es opcional (si no subes, se conserva).</div>
            </div>

          </div>

          <hr class="my-4">

          <div class="d-flex justify-content-center gap-2">
            <button class="btn btn-success px-4" type="submit">GUARDAR</button>
            <a class="btn btn-secondary px-4" href="index.php?mod=marca">REGRESAR</a>
          </div>

        </form>

      </div>
    </div>';

    return $html;
  }

  // ========================= LISTA =========================
  public function get_list(){

    $d_new = base64_encode("new/0");

    $html = '
    <div class="card shadow-sm">
      <div class="card-header d-flex justify-content-between align-items-center bg-dark text-white">
        <span class="fw-bold">LISTA DE MARCAS</span>
        <a class="btn btn-success btn-sm" href="index.php?mod=marca&d='.$d_new.'">+ NUEVO</a>
      </div>

      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-striped table-hover align-middle mb-0">
            <thead class="table-secondary">
              <tr>
                <th>Descripción</th>
                <th>País</th>
                <th>Dirección</th>
                <th>Foto</th>
                <th class="text-center" colspan="3">Acciones</th>
              </tr>
            </thead>
            <tbody>';

    $sql = "SELECT id, descripcion, pais, direccion, foto FROM marca;";
    $res = $this->con->query($sql);

    if(!$res){
      return $this->_message_error("listar<br><br>".$this->con->error);
    }

    if($res->num_rows == 0){
      $html .= '
              <tr>
                <td colspan="7" class="text-center fw-semibold">NO existen registros en la tabla Marca.</td>
              </tr>';
    }else{
      while($row = $res->fetch_assoc()){

        $d_del = base64_encode("del/".$row['id']);
        $d_act = base64_encode("act/".$row['id']);
        $d_det = base64_encode("det/".$row['id']);

        $html .= '
              <tr>
                <td>'.$row['descripcion'].'</td>
                <td>'.$row['pais'].'</td>
                <td>'.$row['direccion'].'</td>
                <td>'.$row['foto'].'</td>

                <td class="text-center">
                  <a class="btn btn-outline-danger btn-sm" href="index.php?mod=marca&d='.$d_del.'">Borrar</a>
                </td>
                <td class="text-center">
                  <a class="btn btn-outline-primary btn-sm" href="index.php?mod=marca&d='.$d_act.'">Actualizar</a>
                </td>
                <td class="text-center">
                  <a class="btn btn-outline-dark btn-sm" href="index.php?mod=marca&d='.$d_det.'">Detalle</a>
                </td>
              </tr>';
      }
    }

    $html .= '
            </tbody>
          </table>
        </div>
      </div>
    </div>';

    return $html;
  }

  // ========================= DETALLE =========================
  public function get_detail_marca($id){

    $sql = "SELECT descripcion, pais, direccion, foto FROM marca WHERE id=$id;";
    $res = $this->con->query($sql);

    if(!$res || $res->num_rows==0){
      return $this->_message_error("detalle<br><br>".$this->con->error);
    }

    $row = $res->fetch_assoc();

    $html = '
    <div class="card shadow-sm">
      <div class="card-header bg-dark text-white fw-bold">DETALLE MARCA</div>

      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-6"><span class="fw-semibold">Descripción:</span> '.$row['descripcion'].'</div>
          <div class="col-md-6"><span class="fw-semibold">País:</span> '.$row['pais'].'</div>
          <div class="col-12"><span class="fw-semibold">Dirección:</span> '.$row['direccion'].'</div>
        </div>

        <hr class="my-4">

        <div class="text-center">
          <img class="img-fluid rounded border" src="./imagenes/'.$row['foto'].'" style="max-width:300px">
        </div>

        <hr class="my-4">

        <div class="text-center">
          <a class="btn btn-secondary px-4" href="index.php?mod=marca">REGRESAR</a>
        </div>
      </div>
    </div>';

    return $html;
  }

  // ========================= BORRAR =========================
  public function delete_marca($id){
    $sql = "DELETE FROM marca WHERE id=$id;";
    if($this->con->query($sql)){
      return $this->_message_ok("ELIMINÓ");
    }else{
      return $this->_message_error("eliminar<br><br>".$this->con->error);
    }
  }

  // ========================= MENSAJES =========================
  private function _message_error($tipo){
    return '
    <div class="alert alert-danger shadow-sm" role="alert">
      <div class="fw-bold mb-1">Error al '.$tipo.' Favor contactar a ....................</div>
      <hr>
      <a class="btn btn-outline-danger btn-sm" href="index.php?mod=marca">Regresar</a>
    </div>';
  }

  private function _message_ok($tipo){
    return '
    <div class="alert alert-success shadow-sm" role="alert">
      <div class="fw-bold mb-1">El registro se '.$tipo.' correctamente</div>
      <hr>
      <a class="btn btn-outline-success btn-sm" href="index.php?mod=marca">Regresar</a>
    </div>';
  }

} // FIN CLASE
?>
