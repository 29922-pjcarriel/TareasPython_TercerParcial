<?php
// =====================================================
// vehiculos.php
// LISTADO + CRUD VEHÍCULOS
// AGENTE (R)  -> puede ver + CONSULTAR
// ADM (CRUD)  -> CRUD completo (SIN consultar matrículas)
// =====================================================

session_start();

// -----------------------------------------------------
// Validar sesión y rol
// -----------------------------------------------------
if (!isset($_SESSION["rol"]) || !in_array($_SESSION["rol"], ["R", "CRUD"])) {
    die("Acceso denegado.");
}

$rol = $_SESSION["rol"];

require_once(__DIR__ . "/../conexion/conexion_matriculacion.php");

// -----------------------------------------------------
// CONSULTA DE VEHÍCULOS
// -----------------------------------------------------
$sql = "
SELECT 
    v.id,
    v.placa,
    m.descripcion AS marca,
    v.motor,
    v.chasis,
    v.combustible,
    v.anio,
    c.descripcion AS color,
    v.avaluo
FROM vehiculo v
JOIN marca m ON v.marca = m.id
JOIN color c ON v.color = c.id
ORDER BY v.id
";

$stmt = $cnMatriculacion->prepare($sql);
$stmt->execute();
$vehiculos = $stmt->fetchAll();
?>
<!doctype html>
<html lang="es">

<head>
    <meta charset="utf-8">
    <title>CRUD Vehículos</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap -->
    <link rel="stylesheet"
        href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">

    <!-- Estilos propios -->
    <link rel="stylesheet" href="../Recursos/css/estilos.css">
</head>

<body>

    <div class="container-fluid" style="margin-top:20px;">

        <div class="row">
            <div class="col-xs-12">
                <h2>Listado de Vehículos</h2>
                <p>
                    Usuario: <strong><?= htmlspecialchars($_SESSION["username"]) ?></strong>
                    | Rol: <strong><?= ($rol === "R" ? "AGENTE" : "ADM") ?></strong>
                </p>
                <hr>
            </div>
        </div>

        <!-- BOTÓN CREAR (solo ADM) -->
        <?php if ($rol === "CRUD") : ?>
            <div class="row" style="margin-bottom:10px;">
                <div class="col-xs-12">
                    <a href="vehiculo_form.php" class="btn btn-success">
                        <span class="glyphicon glyphicon-plus"></span> Nuevo Vehículo
                    </a>
                </div>
            </div>
        <?php endif; ?>

        <!-- TABLA -->
        <div class="row">
            <div class="col-xs-12">
                <div class="table-responsive">
                    <table class="table table-bordered table-striped table-hover">

                        <thead class="bg-success">
                            <tr>
                                <th>ID</th>
                                <th>Placa</th>
                                <th>Marca</th>
                                <th>Motor</th>
                                <th>Chasis</th>
                                <th>Combustible</th>
                                <th>Año</th>
                                <th>Color</th>
                                <th>Avalúo</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>

                        <tbody>
                            <?php if (count($vehiculos) === 0) : ?>
                                <tr>
                                    <td colspan="10" class="text-center">
                                        No existen vehículos registrados.
                                    </td>
                                </tr>
                            <?php else : ?>
                                <?php foreach ($vehiculos as $v) : ?>
                                    <tr>
                                        <td><?= $v["id"] ?></td>
                                        <td><?= htmlspecialchars($v["placa"]) ?></td>
                                        <td><?= htmlspecialchars($v["marca"]) ?></td>
                                        <td><?= htmlspecialchars($v["motor"]) ?></td>
                                        <td><?= htmlspecialchars($v["chasis"]) ?></td>
                                        <td><?= htmlspecialchars($v["combustible"]) ?></td>
                                        <td><?= $v["anio"] ?></td>
                                        <td><?= htmlspecialchars($v["color"]) ?></td>
                                        <td>$ <?= number_format($v["avaluo"], 2) ?></td>

                                        <td>
                                            <!-- BOTONES ADM -->
                                            <?php if ($rol === "CRUD") : ?>
                                                <a href="vehiculo_form.php?id=<?= $v["id"] ?>"
                                                    class="btn btn-xs btn-primary">
                                                    Editar
                                                </a>

                                                <a href="vehiculo_delete.php?id=<?= $v["id"] ?>"
                                                    class="btn btn-xs btn-danger"
                                                    onclick="return confirm('¿Eliminar vehículo?');">
                                                    Eliminar
                                                </a>
                                            <?php endif; ?>

                                            <!-- BOTÓN CONSULTAR (solo AGENTE) -->
                                            <?php if ($rol === "R") : ?>
                                                <a href="../matriculas/consultar_matricula.php?id=<?= $v["id"] ?>">
                                                    CONSULTAR
                                                </a>

                                            <?php endif; ?>
                                        </td>
                                    </tr>
                                <?php endforeach; ?>
                            <?php endif; ?>
                        </tbody>

                    </table>
                </div>
            </div>
        </div>

        <!-- VOLVER -->
        <div class="row">
            <div class="col-xs-12">
                <a href="../index.php" class="btn btn-default">
                    Volver al Inicio
                </a>
            </div>
        </div>

    </div>

</body>

</html>