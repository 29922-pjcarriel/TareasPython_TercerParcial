<?php
// =====================================================
// usuarios/crear_usuario.php
// SOLO SUPERADMIN (rol = C)
// Puede crear usuarios AGENTE y ADMIN
// Password fijo = 123
// =====================================================

session_start();

// -----------------------------------------------------
// Validar acceso (solo SUPERADMIN)
// -----------------------------------------------------
if (!isset($_SESSION["rol"]) || $_SESSION["rol"] !== "C") {
    header("Location: ../index.php");
    exit;
}

require_once(__DIR__ . "/../conexion/conexion_usuarios.php");

$mensaje = "";
$error   = "";

// -----------------------------------------------------
// PROCESAR FORMULARIO
// -----------------------------------------------------
if ($_SERVER["REQUEST_METHOD"] === "POST") {

    $username = trim($_POST["username"] ?? "");
    $rol_id   = $_POST["rol_id"] ?? "";

    if ($username === "" || $rol_id === "") {
        $error = "Todos los campos son obligatorios.";
    } else {

        // ---------------------------------------------
        // Validar rol permitido (AGENTE o ADMIN)
        // ---------------------------------------------
        if (!in_array($rol_id, ["2", "5"])) {
            $error = "Rol no permitido.";
        } else {

            // ---------------------------------------------
            // Verificar username NO repetido
            // ---------------------------------------------
            $sql = "SELECT COUNT(*) FROM usuarios WHERE username = ?";
            $stmt = $cnUsuarios->prepare($sql);
            $stmt->execute([$username]);

            if ($stmt->fetchColumn() > 0) {
                $error = "El username ya existe. No se permiten duplicados.";
            } else {

                // ---------------------------------------------
                // Insertar usuario
                // ---------------------------------------------
                $sql = "
                    INSERT INTO usuarios (username, password, roles_id)
                    VALUES (?, '123', ?)
                ";
                $stmt = $cnUsuarios->prepare($sql);
                $stmt->execute([$username, $rol_id]);

                $mensaje = "Usuario creado correctamente.";
            }
        }
    }
}
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Crear Usuario - SUPERADMIN</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap -->
    <link rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">

    <!-- Estilos -->
    <link rel="stylesheet" href="../Recursos/css/estilos.css">
</head>

<body>

<div class="container" style="margin-top:30px; max-width:600px;">

    <div class="panel panel-success">
        <div class="panel-heading text-center">
            <h3 class="panel-title">
                Crear Usuario (SUPERADMIN)
            </h3>
        </div>

        <div class="panel-body">

            <?php if ($error): ?>
                <div class="alert alert-danger text-center">
                    <?= htmlspecialchars($error) ?>
                </div>
            <?php endif; ?>

            <?php if ($mensaje): ?>
                <div class="alert alert-success text-center">
                    <?= htmlspecialchars($mensaje) ?>
                </div>
            <?php endif; ?>

            <form method="post" action="crear_usuario.php">

                <!-- USERNAME -->
                <div class="form-group">
                    <label>Username</label>
                    <input
                        type="text"
                        name="username"
                        class="form-control"
                        placeholder="Ej: PCH3465 o JuanPerez"
                        required
                    >
                </div>

                <!-- ROL -->
                <div class="form-group">
                    <label>Rol</label>
                    <select name="rol_id" class="form-control" required>
                        <option value="">-- Seleccione un rol --</option>
                        <option value="2">AGENTE</option>
                        <option value="5">ADMINISTRADOR</option>
                    </select>
                </div>

                <!-- PASSWORD -->
                <div class="form-group">
                    <label>Password</label>
                    <input
                        type="text"
                        class="form-control"
                        value="123"
                        disabled
                    >
                    <small class="text-muted">
                        La contraseña por defecto es <b>123</b> para todos los usuarios.
                    </small>
                </div>

                <!-- BOTONES -->
                <button type="submit" class="btn btn-success btn-block">
                    <span class="glyphicon glyphicon-plus"></span>
                    Crear Usuario
                </button>

                <a href="../index.php"
                   class="btn btn-default btn-block"
                   style="margin-top:10px;">
                    Volver al Inicio
                </a>

            </form>

        </div>
    </div>

</div>

</body>
</html>
