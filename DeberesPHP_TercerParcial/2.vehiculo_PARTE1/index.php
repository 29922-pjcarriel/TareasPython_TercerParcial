<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Vehículos</title>

    <!-- Bootstrap 5 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body class="bg-light">

<!-- NAVBAR -->
<nav class="navbar navbar-dark bg-dark">
    <div class="container-fluid">
        <span class="navbar-brand mb-0 h1">Vehículos</span>
    </div>
</nav>

<div class="container mt-4">

    <h2 class="mb-3">Módulo Vehículo</h2>

    <div class="card shadow-sm">
        <div class="card-body">

            <?php
                require_once("class.vehiculo.php");

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
                        case "C":
                            echo $objetoVehiculo->get_form($id);
                            break;
                        case "R":
                            break;
                        case "U":
                            break;
                        case "D":
                            break;
                    }
                } else {
                    // LISTADO ORIGINAL
                    echo "<pre>";
                        print_r($_POST);
                    echo "</pre>";
                    echo "<div class='table-responsive'>";
                    echo $objetoVehiculo->get_list();
                    echo "</div>";
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

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
