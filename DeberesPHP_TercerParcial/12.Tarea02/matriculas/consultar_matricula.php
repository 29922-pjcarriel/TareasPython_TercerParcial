<?php
// =====================================================
// consultar_matricula.php
// SOLO AGENTE
// Guarda el vehículo en SESIÓN
// =====================================================

session_start();

// Solo AGENTE
if (!isset($_SESSION["rol"]) || $_SESSION["rol"] !== "R") {
    header("Location: ../index.php");
    exit;
}

// Validar ID
if (!isset($_GET["id"]) || !is_numeric($_GET["id"])) {
    $_SESSION["msg"] = "Debe seleccionar un vehículo válido.";
    header("Location: ../vehiculos/vehiculos.php");
    exit;
}

// Guardar contexto
$_SESSION["vehiculo_id"] = (int) $_GET["id"];

// Redirigir a la vista
header("Location: ver_matriculas.php");
exit;
