<?php
// =====================================================
// vehiculo_form.php
// FORMULARIO CREAR / EDITAR VEHÍCULO
// SOLO ADM (rol = CRUD)
// =====================================================

session_start();

// -----------------------------------------------------
// Validar acceso (solo ADM)
// -----------------------------------------------------
if (!isset($_SESSION["rol"]) || $_SESSION["rol"] !== "CRUD") {
    header("Location: ../index.php");
    exit;
}

require_once(__DIR__ . "/../conexion/conexion_matriculacion.php");

// -----------------------------------------------------
// Variables
// -----------------------------------------------------
$id = $_GET["id"] ?? null;
$vehiculo = null;

// -----------------------------------------------------
// Cargar marcas y colores
// -----------------------------------------------------
$marcas = $cnMatriculacion->query("SELECT id, descripcion FROM marca")->fetchAll();
$colores = $cnMatriculacion->query("SELECT id, descripcion FROM color")->fetchAll();

// -----------------------------------------------------
// Si es edición, cargar vehículo
// -----------------------------------------------------
if ($id) {
    $sql = "SELECT * FROM vehiculo WHERE id = ?";
    $stmt = $cnMatriculacion->prepare($sql);
    $stmt->execute([$id]);
    $vehiculo = $stmt->fetch();

    if (!$vehiculo) {
        die("Vehículo no encontrado.");
    }
}

// -----------------------------------------------------
// GUARDAR (INSERT / UPDATE)
// -----------------------------------------------------
if ($_SERVER["REQUEST_METHOD"] === "POST") {

    $placa       = $_POST["placa"];
    $marca       = $_POST["marca"];
    $motor       = $_POST["motor"];
    $chasis      = $_POST["chasis"];
    $combustible = $_POST["combustible"];
    $anio        = $_POST["anio"];
    $color       = $_POST["color"];
    $avaluo      = $_POST["avaluo"];

    if ($id) {
        // UPDATE
        $sql = "
            UPDATE vehiculo
            SET placa=?, marca=?, motor=?, chasis=?, combustible=?,
                anio=?, color=?, avaluo=?
            WHERE id=?
        ";
        $stmt = $cnMatriculacion->prepare($sql);
        $stmt->execute([
            $placa,
            $marca,
            $motor,
            $chasis,
            $combustible,
            $anio,
            $color,
            $avaluo,
            $id
        ]);
    } else {
        // INSERT
        $sql = "
            INSERT INTO vehiculo
            (placa, marca, motor, chasis, combustible, anio, color, avaluo, foto)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, '')
        ";
        $stmt = $cnMatriculacion->prepare($sql);
        $stmt->execute([
            $placa,
            $marca,
            $motor,
            $chasis,
            $combustible,
            $anio,
            $color,
            $avaluo
        ]);
    }

    header("Location: vehiculos.php");
    exit;
}
?>
<!doctype html>
<html lang="es">

<head>
    <meta charset="utf-8">
    <title><?= $id ? "Editar" : "Nuevo" ?> Vehículo</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet"
        href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="../Recursos/css/estilos.css">
</head>

<body>

    <div class="container" style="margin-top:30px; max-width:800px;">

        <h3><?= $id ? "Editar Vehículo" : "Registrar Nuevo Vehículo" ?></h3>
        <hr>

        <form method="post">

            <div class="form-group">
                <label>Placa</label>
                <input type="text" name="placa" class="form-control"
                    value="<?= $vehiculo["placa"] ?? "" ?>" required>
            </div>

            <div class="form-group">
                <label>Marca</label>
                <select name="marca" class="form-control" required>
                    <?php foreach ($marcas as $m): ?>
                        <option value="<?= $m["id"] ?>"
                            <?= ($vehiculo && $vehiculo["marca"] == $m["id"]) ? "selected" : "" ?>>
                            <?= $m["descripcion"] ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="form-group">
                <label>Motor</label>
                <input type="text" name="motor" class="form-control"
                    value="<?= $vehiculo["motor"] ?? "" ?>" required>
            </div>

            <div class="form-group">
                <label>Chasis</label>
                <input type="text" name="chasis" class="form-control"
                    value="<?= $vehiculo["chasis"] ?? "" ?>" required>
            </div>

            <div class="form-group">
                <label>Combustible</label>
                <select name="combustible" class="form-control" required>
                    <?php
                    $combustibles = ["Gasolina", "Diésel", "Eléctrico", "Híbrido"];
                    foreach ($combustibles as $c):
                    ?>
                        <option value="<?= $c ?>"
                            <?= (isset($vehiculo) && $vehiculo["combustible"] === $c) ? "selected" : "" ?>>
                            <?= $c ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>


            <div class="form-group">
                <label>Año</label>
                <input type="number" name="anio" class="form-control"
                    value="<?= $vehiculo["anio"] ?? "" ?>" required>
            </div>

            <div class="form-group">
                <label>Color</label>
                <select name="color" class="form-control" required>
                    <?php foreach ($colores as $c): ?>
                        <option value="<?= $c["id"] ?>"
                            <?= ($vehiculo && $vehiculo["color"] == $c["id"]) ? "selected" : "" ?>>
                            <?= $c["descripcion"] ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="form-group">
                <label>Avalúo</label>
                <input type="number" step="0.01" name="avaluo" class="form-control"
                    value="<?= $vehiculo["avaluo"] ?? "" ?>" required>
            </div>

            <button class="btn btn-success">
                <?= $id ? "Actualizar" : "Guardar" ?>
            </button>

            <a href="vehiculos.php" class="btn btn-default">Cancelar</a>

        </form>

    </div>

</body>

</html>