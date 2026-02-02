<?php
// =====================================================
// matriculas/consultar_matricula.php
// SOLO AGENTE (rol = R)
// Guarda el ID del vehículo en SESIÓN y redirige a ver_matriculas.php
// Si NO viene id, redirige a vehiculos.php con mensaje (por SESIÓN)
// =====================================================

session_start();

// -----------------------------------------------------
// Validar acceso (solo AGENTE)
// -----------------------------------------------------
if (!isset($_SESSION["rol"]) || $_SESSION["rol"] !== "R") {
    // Mejor redirigir al inicio en vez de die()
    header("Location: ../index.php");
    exit;
}

// -----------------------------------------------------
// Si NO viene id válido => regresar a vehículos con mensaje
// -----------------------------------------------------
if (!isset($_GET["id"]) || !is_numeric($_GET["id"])) {

    // Mensaje para mostrar en vehiculos.php (lo estás leyendo ahí con $_SESSION["msg_consultar"])
    $_SESSION["msg_consultar"] = "Para consultar matrículas debes seleccionar un vehículo desde la lista.";

    header("Location: ../vehiculos/vehiculos.php");
    exit;
}

// -----------------------------------------------------
// Guardar ID del vehículo en sesión
// -----------------------------------------------------
$_SESSION["vehiculo_id"] = (int) $_GET["id"];

// -----------------------------------------------------
// Redirigir a la vista de matrículas
// -----------------------------------------------------
header("Location: ver_matriculas.php");
exit;
