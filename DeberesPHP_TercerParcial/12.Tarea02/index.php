<?php
// =====================================================
// index.php
// LOGIN + HOME DINÁMICO SEGÚN ROL (SESIONES)
// =====================================================

session_start();

// -----------------------------------------------------
// CARGAR CONEXIÓN A usuariosdb (SIEMPRE)
// -----------------------------------------------------
require_once(__DIR__ . "/conexion/conexion_usuarios.php");

// -----------------------------------------------------
// Variables de sesión
// -----------------------------------------------------
$rol = $_SESSION["rol"] ?? null;        // R | CRUD | C
$username_sesion = $_SESSION["username"] ?? null;

$error = "";

// -----------------------------------------------------
// LOGIN
// -----------------------------------------------------
if ($_SERVER["REQUEST_METHOD"] === "POST"
    && isset($_POST["accion"])
    && $_POST["accion"] === "login"
) {

    $user = trim($_POST["username"] ?? "");
    $pass = trim($_POST["password"] ?? "");

    if ($user === "" || $pass === "") {
        $error = "Debe ingresar usuario y contraseña.";
    } else {

        $sql = "
            SELECT u.username, r.rol
            FROM usuarios u
            JOIN roles r ON u.roles_id = r.id
            WHERE u.username = ? AND u.password = ?
            LIMIT 1
        ";

        $stmt = $cnUsuarios->prepare($sql);
        $stmt->execute([$user, $pass]);
        $row = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($row) {
            $_SESSION["username"] = $row["username"];
            $_SESSION["rol"] = $row["rol"];

            header("Location: index.php");
            exit;
        } else {
            $error = "Usuario o contraseña incorrectos.";
        }
    }
}

// -----------------------------------------------------
// LOGOUT
// -----------------------------------------------------
if (isset($_GET["logout"]) && $_GET["logout"] == "1") {
    session_unset();
    session_destroy();
    header("Location: index.php");
    exit;
}

// -----------------------------------------------------
// Nombre de rol (para mostrar)
// -----------------------------------------------------
$rolNombre = "INVITADO";
if ($rol === "R")    $rolNombre = "AGENTE";
if ($rol === "CRUD") $rolNombre = "ADM";
if ($rol === "C")    $rolNombre = "SUPERADM";
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Prueba</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap -->
    <link rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">

    <!-- Estilos -->
    <link rel="stylesheet" href="Recursos/css/estilos.css">
    <link rel="stylesheet" href="Recursos/icons/style.css">
</head>

<body>

<!-- HEADER -->
<div class="container-fluid">
    <div class="row">
        <header class="col-xs-12">
            <div id="header" class="box white text-center">
                <img src="Recursos/img/logo_ESPE.png"
                     class="img-responsive center-block"
                     style="max-height:100px"
                     alt="ESPE">
            </div>
        </header>
    </div>
</div>

<!-- NAVBAR -->
<nav class="navbar navbar-inverse">
    <div class="container-fluid">

        <div class="navbar-header">
            <button type="button" class="navbar-toggle"
                    data-toggle="collapse" data-target="#main-nav">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <span class="navbar-brand">Grupo 3</span>
        </div>

        <div class="collapse navbar-collapse" id="main-nav">
            <ul class="nav navbar-nav">
                <?php if ($rol === "R"): ?>
                    <li><a href="vehiculos/vehiculos.php">CRUD VEHÍCULOS</a></li>
                    <li><a href="matriculas/consultar_matricula.php">CONSULTAR</a></li>


                <?php elseif ($rol === "CRUD"): ?>
                    <li><a href="vehiculos/vehiculos.php">CRUD VEHÍCULOS</a></li>
                    <li><a href="marcas/marca.php">CRUD MARCAS</a></li>
                    <li><a href="agencias/agencia.php">CRUD AGENCIAS</a></li>

                <?php elseif ($rol === "C"): ?>
                    <li><a href="usuarios/crear_usuario.php">CREAR USUARIOS</a></li>
                <?php endif; ?>
            </ul>

            <p class="navbar-text navbar-right">
                <?php if ($rol): ?>
                    <?= htmlspecialchars($username_sesion) ?> |
                    <strong><?= $rolNombre ?></strong>
                <?php else: ?>
                    NO AUTENTICADO
                <?php endif; ?>
            </p>
        </div>
    </div>
</nav>

<!-- CONTENIDO -->
<div class="container-fluid">
    <div class="row">

        <!-- LEFT -->
        <aside class="col-sm-3">
            <div class="box white">

                <?php if (!$rol): ?>
                    <h4 class="text-center">LOGIN</h4>

                    <?php if ($error): ?>
                        <div class="alert alert-danger"><?= $error ?></div>
                    <?php endif; ?>

                    <form method="post">
                        <input type="hidden" name="accion" value="login">

                        <div class="form-group">
                            <label>Usuario</label>
                            <input name="username" class="form-control" required>
                        </div>

                        <div class="form-group">
                            <label>Password</label>
                            <input name="password" type="password"
                                   class="form-control" value="123" required>
                        </div>

                        <button class="btn btn-success btn-block">
                            Ingresar
                        </button>
                    </form>

                <?php else: ?>
                    <a href="logout.php" class="btn btn-danger btn-block">
                        Cerrar Sesión
                    </a>
                <?php endif; ?>

            </div>
        </aside>

        <!-- CENTER -->
        <main class="col-sm-6">
            <div class="box soft-green">
                <h2>Aplicación de Tecnologías WEB</h2>

                <?php if ($rol): ?>
                    <p><strong>Usuario:</strong> <?= $username_sesion ?></p>
                    <p><strong>Rol:</strong> <?= $rolNombre ?></p>
                <?php else: ?>
                    <p>Inicia sesión para continuar.</p>
                <?php endif; ?>

                <hr>
                <p>Estudiantes: Pamela Carriel, Karla Molina, Josue Tapia</p>
                <p>NRC: 29922</p>
                <p>Grupo 05</p>
                <p>Fecha: 30 de octubre del 2025</p>
            </div>
        </main>

        <!-- RIGHT -->
        <section class="col-sm-3">
            <div class="box dark-green">
                <iframe width="100%" height="200"
                        src="https://www.youtube.com/embed/_mLQ4BaMPoY?autoplay=1&mute=1"
                        frameborder="0"
                        allowfullscreen></iframe>
            </div>
        </section>

    </div>
</div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
</body>
</html>
