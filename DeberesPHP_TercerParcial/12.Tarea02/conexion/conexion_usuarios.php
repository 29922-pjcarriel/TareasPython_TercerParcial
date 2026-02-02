<?php
// =====================================================
// conexion_usuarios.php
// CONEXIÓN A LA BASE DE DATOS usuariosdb
// =====================================================

// Datos de conexión
$host = "localhost";
$db   = "usuariosdb";
$user = "root";
$pass = "123";          // XAMPP / WAMP normalmente vacío
$charset = "utf8";

// DSN
$dsn = "mysql:host=$host;dbname=$db;charset=$charset";

try {
    // Crear conexión PDO
    $cnUsuarios = new PDO($dsn, $user, $pass);

    // Modo de errores
    $cnUsuarios->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Fetch asociativo por defecto
    $cnUsuarios->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

} catch (PDOException $e) {
    // Error crítico de conexión
    die("Error de conexión a usuariosdb: " . $e->getMessage());
}
