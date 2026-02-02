<?php
// =====================================================
// ver_matriculas.php
// Muestra las matrículas de un vehículo
// SOLO AGENTE (rol = R)
// Usa el ID del vehículo guardado en SESIÓN
// =====================================================

session_start();

// -----------------------------------------------------
// Validar acceso (solo AGENTE)
// -----------------------------------------------------
if (!isset($_SESSION["rol"]) || $_SESSION["rol"] !== "R") {
    die("Acceso denegado. Solo el rol AGENTE puede consultar matrículas.");
}

// -----------------------------------------------------
// Validar que exista el vehículo en sesión
// -----------------------------------------------------
if (!isset($_SESSION["vehiculo_id"])) {
    die("No se ha seleccionado ningún vehículo para consultar.");
}

$vehiculo_id = $_SESSION["vehiculo_id"];

require_once(__DIR__ . "/../conexion/conexion_matriculacion.php");

// -----------------------------------------------------
// Obtener información del vehículo
// -----------------------------------------------------
$sqlVehiculo = "
    SELECT 
        v.placa,
        m.descripcion AS marca,
        v.anio
    FROM vehiculo v
    JOIN marca m ON v.marca = m.id
    WHERE v.id = ?
";

$stmtVeh = $cnMatriculacion->prepare($sqlVehiculo);
$stmtVeh->execute([$vehiculo_id]);
$vehiculo = $stmtVeh->fetch();

if (!$vehiculo) {
    die("Vehículo no encontrado.");
}

// -----------------------------------------------------
// Obtener matrículas del vehículo (solo años matriculados)
// -----------------------------------------------------
$sqlMatriculas = "
    SELECT 
        m.anio,
        m.fecha,
        a.descripcion AS agencia
    FROM matricula m
    JOIN agencia a ON m.agencia = a.id
    WHERE m.vehiculo = ?
    ORDER BY m.anio
";

$stmtMat = $cnMatriculacion->prepare($sqlMatriculas);
$stmtMat->execute([$vehiculo_id]);
$matriculas = $stmtMat->fetchAll();
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Consulta de Matrículas</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap -->
    <link rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">

    <!-- Estilos -->
    <link rel="stylesheet" href="../Recursos/css/estilos.css">
</head>

<body>

<div class="container" style="margin-top:30px; max-width:900px;">

    <div class="panel panel-success">
        <div class="panel-heading">
            <h3 class="panel-title">Consulta de Matrículas</h3>
        </div>

        <div class="panel-body">

            <!-- Información del vehículo -->
            <h4>Información del Vehículo</h4>
            <table class="table table-bordered">
                <tr>
                    <th>Placa</th>
                    <td><?= htmlspecialchars($vehiculo["placa"]) ?></td>
                </tr>
                <tr>
                    <th>Marca</th>
                    <td><?= htmlspecialchars($vehiculo["marca"]) ?></td>
                </tr>
                <tr>
                    <th>Año</th>
                    <td><?= $vehiculo["anio"] ?></td>
                </tr>
            </table>

            <hr>

            <!-- Matrículas -->
            <h4>Historial de Matrículas</h4>

            <?php if (count($matriculas) === 0) : ?>
                <div class="alert alert-warning">
                    Este vehículo no registra matrículas.
                </div>
            <?php else : ?>
                <div class="table-responsive">
                    <table class="table table-striped table-bordered">
                        <thead class="bg-success">
                            <tr>
                                <th>Año</th>
                                <th>Fecha</th>
                                <th>Agencia</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($matriculas as $m) : ?>
                                <tr>
                                    <td><?= $m["anio"] ?></td>
                                    <td><?= $m["fecha"] ?></td>
                                    <td><?= htmlspecialchars($m["agencia"]) ?></td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            <?php endif; ?>

            <hr>

            <!-- Botones -->
            <a href="../vehiculos/vehiculos.php" class="btn btn-default">
                Volver a Vehículos
            </a>

            <a href="../index.php" class="btn btn-primary">
                Inicio
            </a>

        </div>
    </div>

</div>

</body>
</html>
