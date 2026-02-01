<?php
class cliente{
  private $ClienteID;
  private $RazonSocial;
  private $Direccion;
  private $Ciudad;
  private $Estado;
  private $CodigoPostal;
  private $Rif;
  private $Pais;
  private $Telefonos;
  private $con;

  function __construct($cn){
    $this->con = $cn;
  }

  public function save_cliente(){
    $this->RazonSocial = $_POST['RazonSocial'];
    $this->Direccion = $_POST['Direccion'];
    $this->Ciudad = $_POST['Ciudad'];
    $this->Estado = $_POST['Estado'];
    $this->CodigoPostal = $_POST['CodigoPostal'];
    $this->Rif = $_POST['Rif'];
    $this->Pais = $_POST['Pais'];
    $this->Telefonos = $_POST['Telefonos'];

    $sql = "INSERT INTO Clientes VALUES(NULL,
        '$this->RazonSocial',
        '$this->Direccion',
        '$this->Ciudad',
        '$this->Estado',
        '$this->CodigoPostal',
        '$this->Rif',
        '$this->Pais',
        '$this->Telefonos');";

    if($this->con->query($sql)){
      echo $this->_message_ok("guardó");
    }else{
      echo $this->_message_error("guardar");
    }
  }

  public function update_cliente(){
    $this->ClienteID = (int)$_POST['ClienteID'];
    $this->RazonSocial = $_POST['RazonSocial'];
    $this->Direccion = $_POST['Direccion'];
    $this->Ciudad = $_POST['Ciudad'];
    $this->Estado = $_POST['Estado'];
    $this->CodigoPostal = $_POST['CodigoPostal'];
    $this->Rif = $_POST['Rif'];
    $this->Pais = $_POST['Pais'];
    $this->Telefonos = $_POST['Telefonos'];

    $sql = "UPDATE Clientes SET
        RazonSocial='$this->RazonSocial',
        Direccion='$this->Direccion',
        Ciudad='$this->Ciudad',
        Estado='$this->Estado',
        CodigoPostal='$this->CodigoPostal',
        Rif='$this->Rif',
        Pais='$this->Pais',
        Telefonos='$this->Telefonos'
      WHERE ClienteID=$this->ClienteID;";

    if($this->con->query($sql)){
      echo $this->_message_ok("modificó");
    }else{
      echo $this->_message_error("al modificar");
    }
  }

  public function delete_cliente($id){
    $sql = "DELETE FROM Clientes WHERE ClienteID=$id;";
    if($this->con->query($sql)){
      echo $this->_message_ok("ELIMINÓ");
    }else{
      echo $this->_message_error("eliminar");
    }
  }

  public function get_form($id=NULL){

    if($id == NULL){
      $this->RazonSocial = NULL;
      $this->Direccion = NULL;
      $this->Ciudad = NULL;
      $this->Estado = NULL;
      $this->CodigoPostal = NULL;
      $this->Rif = NULL;
      $this->Pais = NULL;
      $this->Telefonos = NULL;

      $op = "cnew";
      $titulo = "Nuevo Cliente";
      $ClienteID = 0;

    }else{
      $sql = "SELECT * FROM Clientes WHERE ClienteID=$id;";
      $res = $this->con->query($sql);
      $row = $res->fetch_assoc();

      $num = $res->num_rows;
      if($num==0){
        $mensaje = "tratar de actualizar el cliente con id= ".$id;
        echo $this->_message_error($mensaje);
      }else{
        $ClienteID = $row['ClienteID'];
        $this->RazonSocial = $row['RazonSocial'];
        $this->Direccion = $row['Direccion'];
        $this->Ciudad = $row['Ciudad'];
        $this->Estado = $row['Estado'];
        $this->CodigoPostal = $row['CodigoPostal'];
        $this->Rif = $row['Rif'];
        $this->Pais = $row['Pais'];
        $this->Telefonos = $row['Telefonos'];

        $op = "cupdate";
        $titulo = "Actualizar Cliente";
      }
    }

    $html = '
    <div class="card shadow-sm">
      <div class="card-header bg-dark text-white"><b>'.$titulo.'</b></div>
      <div class="card-body">
        <form method="POST" action="index.php">
          <input type="hidden" name="ClienteID" value="'.$ClienteID.'">
          <input type="hidden" name="op" value="'.$op.'">

          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label">Razón Social</label>
              <input class="form-control" type="text" name="RazonSocial" value="'.$this->RazonSocial.'">
            </div>
            <div class="col-md-6">
              <label class="form-label">RIF</label>
              <input class="form-control" type="text" name="Rif" value="'.$this->Rif.'">
            </div>
            <div class="col-md-12">
              <label class="form-label">Dirección</label>
              <input class="form-control" type="text" name="Direccion" value="'.$this->Direccion.'">
            </div>
            <div class="col-md-4">
              <label class="form-label">Ciudad</label>
              <input class="form-control" type="text" name="Ciudad" value="'.$this->Ciudad.'">
            </div>
            <div class="col-md-4">
              <label class="form-label">Estado</label>
              <input class="form-control" type="text" name="Estado" value="'.$this->Estado.'">
            </div>
            <div class="col-md-4">
              <label class="form-label">Código Postal</label>
              <input class="form-control" type="text" name="CodigoPostal" value="'.$this->CodigoPostal.'">
            </div>
            <div class="col-md-6">
              <label class="form-label">País</label>
              <input class="form-control" type="text" name="Pais" value="'.$this->Pais.'">
            </div>
            <div class="col-md-6">
              <label class="form-label">Teléfonos</label>
              <input class="form-control" type="text" name="Telefonos" value="'.$this->Telefonos.'">
            </div>
          </div>

          <div class="d-flex gap-2 mt-3">
            <input class="btn btn-primary" type="submit" name="Guardar" value="GUARDAR">
            <a class="btn btn-outline-secondary" href="index.php?d='.base64_encode("clist/0").'">Regresar</a>
          </div>
        </form>
      </div>
    </div>';

    return $html;
  }

  public function get_list(){
    $d_new = base64_encode("cnew/0");
    $html = '
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h4 class="m-0">Lista de Clientes</h4>
      <a class="btn btn-success" href="index.php?d='.$d_new.'">Nuevo</a>
    </div>

    <div class="card shadow-sm">
    <div class="table-responsive">
    <table class="table table-striped table-hover align-middle mb-0">
      <thead class="table-dark">
        <tr>
          <th>Razón Social</th>
          <th>Ciudad</th>
          <th>País</th>
          <th>Teléfonos</th>
          <th colspan="3">Acciones</th>
        </tr>
      </thead>
      <tbody>';

    $sql = "SELECT * FROM Clientes ORDER BY ClienteID DESC;";
    $res = $this->con->query($sql);

    while($row = $res->fetch_assoc()){
      $d_del = base64_encode("cdel/".$row['ClienteID']);
      $d_act = base64_encode("cact/".$row['ClienteID']);
      $d_det = base64_encode("cdet/".$row['ClienteID']);

      $html .= '
      <tr>
        <td>'.$row['RazonSocial'].'</td>
        <td>'.$row['Ciudad'].'</td>
        <td>'.$row['Pais'].'</td>
        <td>'.$row['Telefonos'].'</td>
        <td><a class="btn btn-sm btn-outline-danger" href="index.php?d='.$d_del.'">Borrar</a></td>
        <td><a class="btn btn-sm btn-outline-warning" href="index.php?d='.$d_act.'">Actualizar</a></td>
        <td><a class="btn btn-sm btn-outline-info" href="index.php?d='.$d_det.'">Detalle</a></td>
      </tr>';
    }

    $html .= '</tbody></table></div></div>';
    return $html;
  }

  public function get_detail_cliente($id){
    $sql = "SELECT * FROM Clientes WHERE ClienteID=$id;";
    $res = $this->con->query($sql);
    $row = $res->fetch_assoc();

    $num = $res->num_rows;
    if($num==0){
      $mensaje = "tratar de ver detalle del cliente con id= ".$id;
      echo $this->_message_error($mensaje);
    }else{
      $html = '
      <div class="card shadow-sm">
        <div class="card-header bg-dark text-white"><b>Detalle Cliente</b></div>
        <div class="card-body">
          <p><b>Razón Social:</b> '.$row['RazonSocial'].'</p>
          <p><b>Dirección:</b> '.$row['Direccion'].'</p>
          <p><b>Ciudad:</b> '.$row['Ciudad'].'</p>
          <p><b>País:</b> '.$row['Pais'].'</p>
          <p><b>Teléfonos:</b> '.$row['Telefonos'].'</p>
          <a class="btn btn-outline-secondary" href="index.php?d='.base64_encode("clist/0").'">Regresar</a>
        </div>
      </div>';
      return $html;
    }
  }

  public function combo_clientes($defecto=NULL){
    $html = '<select class="form-select" name="ClienteID" required>';
    $html .= '<option value="">-- Seleccione Cliente --</option>';
    $sql = "SELECT ClienteID,RazonSocial FROM Clientes ORDER BY RazonSocial;";
    $res = $this->con->query($sql);
    while($row = $res->fetch_assoc()){
      $sel = ($defecto == $row['ClienteID']) ? "selected" : "";
      $html .= '<option value="'.$row['ClienteID'].'" '.$sel.'>'.$row['RazonSocial'].'</option>';
    }
    $html .= '</select>';
    return $html;
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
