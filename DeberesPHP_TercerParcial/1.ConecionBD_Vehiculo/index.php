<!DOCTYPE html>
<html lang="es">

<head>
	<meta charset="utf-8">
	<title>CRUD Vehículos y Matrículas</title>

	<!-- BOOTSTRAP CSS -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

	<!-- Bootstrap Icons -->
	<link rel="stylesheet"
		href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
</head>

<body class="bg-light">

	<!-- ================= NAVBAR ================= -->
	<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
		<div class="container">
			<a class="navbar-brand" href="index.php">CRUD</a>

			<div class="collapse navbar-collapse show">
				<ul class="navbar-nav me-auto mb-2 mb-lg-0">
					<li class="nav-item">
						<a class="nav-link" href="index.php?m=V">Vehículos</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="index.php?m=M">Matrículas</a>
					</li>
				</ul>
			</div>
		</div>
	</nav>
	<!-- ========================================== -->

	<div class="container mt-4">

	<?php
	// ================= INCLUDES =================
	require_once("class.vehiculo.php");
	require_once("class.matricula.php");

	// ================= CONEXIÓN =================
	function conectar()
	{
		$server = "localhost";
		$user = "root";
		$pass = "123";
		$db = "matriculacionfinal";

		$c = new mysqli($server, $user, $pass, $db);
		$c->set_charset("utf8");
		return $c;
	}

	$db = conectar();

	$objVehiculo  = new vehiculo($db);
	$objMatricula = new matricula($db);

	// ================= CONTROLADOR =================
	if (isset($_GET['m'])) {

		switch ($_GET['m']) {
			case "V":
				echo $objVehiculo->get_list();
				break;

			case "M":
				echo $objMatricula->get_list();
				break;

			default:
				echo $objVehiculo->get_list();
				break;
		}

	} else {
		// Por defecto
		echo $objVehiculo->get_list();
	}

	?>
	</div>

	<!-- BOOTSTRAP JS -->
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
