<?php
// =====================================================
// index.php – FRONT CONTROLLER (VEHÍCULO + MATRÍCULA)
// =====================================================

include_once("routes/constantes.php");
include_once("routes/class_vehiculo.php");
include_once("routes/class_matricula.php");

// =====================================================
// CONEXIÓN BD
// =====================================================
function conectar()
{
    $cn = new mysqli(SERVER, USER, PASS, BD);
    if ($cn->connect_errno) {
        die("Error de conexión");
    }
    $cn->set_charset("utf8");
    return $cn;
}

$cn = conectar();

// =====================================================
// MÓDULO ACTIVO
// =====================================================
$mod = $_GET['mod'] ?? 'vehiculo';

if ($mod === 'matricula') {
    $obj = new Matricula($cn);
} else {
    $mod = 'vehiculo';
    $obj = new Vehiculo($cn);
}

// =====================================================
// HTML + NAVBAR
// =====================================================
?>
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Navbar CRUD</title>

    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
    
    <style>
        body {
            background: #eef1f5;
        }

        .navbar {
            border-radius: 0 0 14px 14px;
        }

        .nav-link.active {
            font-weight: 600;
            background: rgba(255, 255, 255, .15);
            border-radius: 8px;
        }
    </style>
</head>

<body>

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">
        <a class="navbar-brand fw-bold" href="index.php">
            <i class="bi bi-layers"></i> Navbar CRUD
        </a>

        <div class="collapse navbar-collapse">
            <ul class="navbar-nav me-auto">

                <li class="nav-item">
                    <a class="nav-link <?= ($mod === 'vehiculo') ? 'active' : '' ?>"
                        href="index.php?mod=vehiculo">
                        <i class="bi bi-car-front-fill"></i> Vehículos
                    </a>
                </li>

                <li class="nav-item ms-2">
                    <a class="nav-link <?= ($mod === 'matricula') ? 'active' : '' ?>"
                        href="index.php?mod=matricula">
                        <i class="bi bi-journal-check"></i> Matrículas
                    </a>
                </li>

            </ul>
            <span class="navbar-text text-light opacity-75">
                PHP + MySQL
            </span>
        </div>
    </nav>

    <div class="container-fluid mt-3">
        <?php
        // =====================================================
        // POST → GUARDAR
        // =====================================================
        if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['Guardar'])) {

            if ($mod === 'vehiculo') {
                echo $obj->save_vehiculo();
            } else {
                echo $obj->save_matricula();
            }
        }
        // =====================================================
        // GET → OPERACIONES (?d=base64(op/id))
        // =====================================================
        elseif (isset($_GET['d'])) {

            $dato = base64_decode($_GET['d']);
            $tmp  = explode("/", $dato);

            $op = $tmp[0] ?? '';
            $id = intval($tmp[1] ?? 0);

            if ($op === 'new') {
                echo $obj->get_form();
            } elseif ($op === 'act') {
                echo $obj->get_form($id);
            } elseif ($op === 'det') {
                echo ($mod === 'vehiculo')
                    ? $obj->get_detail_vehiculo($id)
                    : $obj->get_detail_matricula($id);
            } elseif ($op === 'del') {
                echo ($mod === 'vehiculo')
                    ? $obj->delete_vehiculo($id)
                    : $obj->delete_matricula($id);
            } else {
                echo "<div class='alert alert-danger'>Operación no válida</div>";
            }
        }
        // =====================================================
        // DEFAULT → LISTA
        // =====================================================
        else {
            echo $obj->get_list();
        }
        ?>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>

</html>