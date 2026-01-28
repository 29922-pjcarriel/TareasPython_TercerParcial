<?php
// =====================================================
// index.php – FRONT CONTROLLER (SOLO VEHÍCULO)
// COMPATIBLE CON class_vehiculo.php
// =====================================================

include_once("routes/constantes.php");
include_once("routes/class_vehiculo.php");

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

$cn  = conectar();

// =====================================================
// MODULO FIJO (vehiculo)
// =====================================================
$mod = 'vehiculo';
$obj = new Vehiculo($cn);
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>CRUD Vehículos</title>

    <!-- BOOTSTRAP -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
</head>

<body class="bg-light">

<div class="container-fluid mt-3">

<?php
// =====================================================
// POST → GUARDAR
// =====================================================
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['Guardar'])) {

    echo $obj->save_vehiculo();
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
    }
    elseif ($op === 'act') {
        echo $obj->get_form($id);
    }
    elseif ($op === 'det') {
        echo $obj->get_detail_vehiculo($id);
    }
    elseif ($op === 'del') {
        echo $obj->delete_vehiculo($id);
    }
    else {
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
