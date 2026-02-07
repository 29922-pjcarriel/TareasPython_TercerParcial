<?php
// =====================================================
// vehiculo_form.php
// FORMULARIO CREAR / EDITAR VEHÍCULO
// SOLO ADM (rol = CRUD)
// CREA AUTOMÁTICAMENTE USUARIO DUEÑO AL INSERTAR
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
$id = isset($_GET["id"]) && is_numeric($_GET["id"]) ? (int)$_GET["id"] : null;
$vehiculo = null;

$mensaje = "";
$error   = "";

// -----------------------------------------------------
// Cargar marcas y colores
// -----------------------------------------------------
$marcas  = $cnMatriculacion->query("SELECT id, descripcion FROM marca ORDER BY descripcion")->fetchAll();
$colores = $cnMatriculacion->query("SELECT id, descripcion FROM color ORDER BY descripcion")->fetchAll();

// -----------------------------------------------------
// Si es edición, cargar vehículo
// -----------------------------------------------------
if ($id) {
    $sql = "SELECT * FROM vehiculo WHERE id = ?";
    $stmt = $cnMatriculacion->prepare($sql);
    $stmt->execute([$id]);
    $vehiculo = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$vehiculo) {
        die("Vehículo no encontrado.");
    }
}

// -----------------------------------------------------
// GUARDAR (INSERT / UPDATE)
// -----------------------------------------------------
if ($_SERVER["REQUEST_METHOD"] === "POST") {

    $placa       = strtoupper(trim($_POST["placa"] ?? ""));
    $marca       = $_POST["marca"] ?? "";
    $motor       = trim($_POST["motor"] ?? "");
    $chasis      = trim($_POST["chasis"] ?? "");
    $combustible = trim($_POST["combustible"] ?? "");
    $anio        = $_POST["anio"] ?? "";
    $color       = $_POST["color"] ?? "";
    $avaluo      = $_POST["avaluo"] ?? "";

    // Validación básica
    if ($placa === "" || $marca === "" || $motor === "" || $chasis === "" || $combustible === "" || $anio === "" || $color === "" || $avaluo === "") {
        $error = "Complete todos los campos.";
    } else {

        if ($id) {
            // ----------------------------
            // UPDATE VEHÍCULO
            // ----------------------------
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
            // -------------------------------------------------
            // VALIDAR PLACA NO REPETIDA EN VEHICULO
            // -------------------------------------------------
            $sqlPlaca = "SELECT COUNT(*) FROM vehiculo WHERE placa = ?";
            $stmtPlaca = $cnMatriculacion->prepare($sqlPlaca);
            $stmtPlaca->execute([$placa]);

            if ($stmtPlaca->fetchColumn() > 0) {
                $error = "La placa ya está registrada en el sistema.";
            } else {

                // ----------------------------
                // INSERT VEHÍCULO
                // ----------------------------
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

                // =====================================================
                // CREAR USUARIO DUEÑO DEL VEHÍCULO (AUTOMÁTICO)
                // username = PLACA | password = 123 | rol = Read (R)
                // OJO: TU BD NO TIENE un rol "Dueño" separado, así que
                // se usa roles_id = 2 (Read = R) y se diferencia por username=placa
                // =====================================================
                require_once(__DIR__ . "/../conexion/conexion_usuarios.php");

                // Verificar que NO exista el usuario
                $sqlCheck = "SELECT COUNT(*) FROM usuarios WHERE username = ?";
                $stmtCheck = $cnUsuarios->prepare($sqlCheck);
                $stmtCheck->execute([$placa]);

                if ($stmtCheck->fetchColumn() == 0) {
                    // Read = R => roles_id = 2 (según tu tabla roles)
                    $sqlUser = "
                        INSERT INTO usuarios (username, password, roles_id)
                        VALUES (?, '123', 2)
                    ";
                    $stmtUser = $cnUsuarios->prepare($sqlUser);
                    $stmtUser->execute([$placa]);
                }
            }
        }

        // Si no hubo error, redirigir
        if ($error === "") {
            header("Location: vehiculos.php");
            exit;
        }
    }
}

// Para repintar el formulario cuando hay error
$formPlaca       = $placa       ?? ($vehiculo["placa"] ?? "");
$formMarca       = $marca       ?? ($vehiculo["marca"] ?? "");
$formMotor       = $motor       ?? ($vehiculo["motor"] ?? "");
$formChasis      = $chasis      ?? ($vehiculo["chasis"] ?? "");
$formCombustible = $combustible ?? ($vehiculo["combustible"] ?? "");
$formAnio        = $anio        ?? ($vehiculo["anio"] ?? "");
$formColor       = $color       ?? ($vehiculo["color"] ?? "");
$formAvaluo      = $avaluo      ?? ($vehiculo["avaluo"] ?? "");
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

    <h3 class="text-center"><?= $id ? "Editar Vehículo" : "Registrar Nuevo Vehículo" ?></h3>
    <hr>

    <?php if ($error !== ""): ?>
        <div class="alert alert-danger">
            <?= htmlspecialchars($error) ?>
        </div>
    <?php endif; ?>

    <form method="post">

        <div class="form-group">
            <label>Placa</label>
            <input type="text" name="placa" class="form-control"
                   value="<?= htmlspecialchars($formPlaca) ?>"
                   placeholder="Ej: PCH3465"
                   required>
        </div>

        <div class="form-group">
            <label>Marca</label>
            <select name="marca" class="form-control" required>
                <option value="">-- Seleccione --</option>
                <?php foreach ($marcas as $m): ?>
                    <option value="<?= $m["id"] ?>"
                        <?= ((string)$formMarca === (string)$m["id"]) ? "selected" : "" ?>>
                        <?= htmlspecialchars($m["descripcion"]) ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>

        <div class="form-group">
            <label>Motor</label>
            <input type="text" name="motor" class="form-control"
                   value="<?= htmlspecialchars($formMotor) ?>" required>
        </div>

        <div class="form-group">
            <label>Chasis</label>
            <input type="text" name="chasis" class="form-control"
                   value="<?= htmlspecialchars($formChasis) ?>" required>
        </div>

        <div class="form-group">
            <label>Combustible</label>
            <select name="combustible" class="form-control" required>
                <?php
                $combustibles = ["Gasolina", "Diésel", "Eléctrico", "Híbrido"];
                foreach ($combustibles as $c):
                ?>
                    <option value="<?= $c ?>"
                        <?= ($formCombustible === $c) ? "selected" : "" ?>>
                        <?= $c ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>

        <div class="form-group">
            <label>Año</label>
            <input type="number" name="anio" class="form-control"
                   value="<?= htmlspecialchars($formAnio) ?>" required>
        </div>

        <div class="form-group">
            <label>Color</label>
            <select name="color" class="form-control" required>
                <option value="">-- Seleccione --</option>
                <?php foreach ($colores as $c): ?>
                    <option value="<?= $c["id"] ?>"
                        <?= ((string)$formColor === (string)$c["id"]) ? "selected" : "" ?>>
                        <?= htmlspecialchars($c["descripcion"]) ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>

        <div class="form-group">
            <label>Avalúo</label>
            <input type="number" step="0.01" name="avaluo" class="form-control"
                   value="<?= htmlspecialchars($formAvaluo) ?>" required>
        </div>

        <button class="btn btn-success">
            <?= $id ? "Actualizar" : "Guardar" ?>
        </button>

        <a href="vehiculos.php" class="btn btn-default">Cancelar</a>

    </form>

</div>

</body>
</html>
