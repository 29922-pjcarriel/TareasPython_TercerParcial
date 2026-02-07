<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Matriculas Vehículos PARTE I</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">

<?php include "navbar.php"; ?>

<div class="container py-4">
  <div class="d-flex align-items-center justify-content-between mb-3">
    <h4 class="mb-0">Módulo Vehículo</h4>
  </div>

  <div class="card shadow-sm">
    <div class="card-body">
      <?php
        require_once("class/class.vehiculo.php");
        
        $db = conectar();
        $objetoVehiculo = new vehiculo($db);

        if(isset($_GET['d'])){
          
          echo "<pre>";
            print_r($_GET);
          echo "</pre>";
     
          $tmp = explode("/", $_GET['d']);
          $op = $tmp[0];
          $id = $tmp[1];

          switch($op){
            case "C": echo $objetoVehiculo->get_form($id);
                      break;
            case "R":
                      break;
            case "U":
                      break;						
            case "D":
                      break;						
          }    

        }else{
          echo "<pre>";
            print_r($_POST);
          echo "</pre>";

          echo $objetoVehiculo->get_list();
        }

        function conectar(){
          $server = "localhost";
          $user = "root";
          $pass = "123";
          $db = "matriculacionfinal";
          $c = new mysqli($server,$user,$pass,$db);
          $c->set_charset("utf8");
          return $c;
        }
      ?>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

<script>
document.querySelectorAll("table").forEach(t=>{
  t.classList.add("table","table-bordered","table-hover","align-middle");
});
document.querySelectorAll('input[type="submit"]').forEach(b=>{
  b.classList.add("btn","btn-success");
});
</script>

</body>
</html>
