<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Matriculas Vehículos - PARTE II</title>

  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body class="bg-light">

<?php
  include_once("constantes.php");
  require_once("class/class.vehiculo.php");
  require_once("class/class.matricula.php");

  $cn = conectar();

  // MODULO ACTIVO (vehiculo / matricula)
  $mod = (isset($_GET['mod'])) ? $_GET['mod'] : 'vehiculo';

  if($mod == "matricula"){
      $obj = new matricula($cn);
  }else{
      $mod = "vehiculo";
      $obj = new vehiculo($cn);
  }
?>

<!-- NAVBAR -->
<nav class="navbar navbar-expand-lg navbar-dark bg-success">
  <div class="container">
    <a class="navbar-brand fw-bold" href="index.php">CRUD Vehículos</a>

    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navMenu">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item">
          <a class="nav-link <?php echo ($mod=="vehiculo")?'active':''; ?>" href="index.php?mod=vehiculo">Vehículo</a>
        </li>
        <li class="nav-item">
          <a class="nav-link <?php echo ($mod=="matricula")?'active':''; ?>" href="index.php?mod=matricula">Matrícula</a>
        </li>
      </ul>
    </div>
  </div>
</nav>


<div class="container my-4">
  <div class="card shadow-sm">
    <div class="card-body">

      <?php
      // ==========================================================
      // SOLO GET: det y del
      // ==========================================================
      if(isset($_GET['d'])){

          $dato = base64_decode($_GET['d']);
          $tmp = explode("/", $dato);

          $op = $tmp[0];
          $id = $tmp[1];

          // =======================
          // MODULO VEHICULO
          // =======================
          if($mod == "vehiculo"){

              if($op == "det"){
                  echo $obj->get_detail_vehiculo($id);

              }elseif($op == "del"){
                  echo $obj->delete_vehiculo($id);

              }else{
                  echo '<div class="alert alert-warning">
                          Solo está habilitado <b>Detalle</b> y <b>Borrar</b>.
                        </div>';
                  echo $obj->get_list();
              }

          // =======================
          // MODULO MATRICULA
          // =======================
          }elseif($mod == "matricula"){

              if($op == "det"){
                  echo $obj->get_detail_matricula($id);

              }elseif($op == "del"){
                  echo $obj->delete_matricula($id);

              }else{
                  echo '<div class="alert alert-warning">
                          Solo está habilitado <b>Detalle</b> y <b>Borrar</b>.
                        </div>';
                  echo $obj->get_list();
              }
          }

      }else{
          // LISTA POR DEFECTO
          echo $obj->get_list();
      }
      ?>

    </div>
  </div>
</div>


<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>

<?php
//*******************************************************
function conectar(){
  //echo "<br> CONEXION A LA BASE DE DATOS<br>";
  $c = new mysqli(SERVER,USER,PASS,BD);

  if($c->connect_errno) {
    die("Error de conexión: " . $c->mysqli_connect_errno() . ", " . $c->connect_error());
  }else{
    //echo "La conexión tuvo éxito .......<br><br>";
  }

  $c->set_charset("utf8");
  return $c;
}
//**********************************************************
?>
