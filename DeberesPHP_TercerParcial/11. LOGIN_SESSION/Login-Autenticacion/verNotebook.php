<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once("Notebook.php");
session_start();

/* ===== VALIDACIONES ===== */
if (!isset($_SESSION['listaNote'])) {
    header("location:index.php");
    exit;
}

$notes = $_SESSION['listaNote'];

if (isset($_POST['op'])) {
    $op = $_POST['op'];
} elseif (isset($_GET['op'])) {
    $op = $_GET['op'];
} else {
    header("location:index.php");
    exit;
}

if (!isset($notes[$op])) {
    header("location:index.php");
    exit;
}

$obj = $notes[$op];
?>
<html>
<head>
	<meta charset="utf-8">
	<title>Bienvenida</title>

	<!-- BOOTSTRAP CSS -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body class="bg-light">

	<div class="container py-5">

		<div class="text-center mb-4">
			<h2 class="fw-bold">BIENVENIDOS !!!!</h2>
		</div>

		<div class="card shadow mx-auto mb-4" style="max-width: 600px;">
			<div class="card-body text-center">
				<h1 class="fw-bold mb-3"><?php echo $obj->getMarca(); ?></h1>

				<p class="fs-4 mb-4">
					Precio: <span class="fw-bold">$<?php echo $obj->getPrecio(); ?></span>
				</p>

				<a href="index.php" class="btn btn-primary">Continuar</a>
			</div>
		</div>

		<!-- IMPRESION DE LA VARIABLE SESSION -->
		<div class="card shadow mx-auto" style="max-width: 600px;">
			<div class="card-body">
				<h5 class="fw-bold">VARIABLE SESSION:</h5>
				<pre class="bg-light border rounded p-3 mb-0"><?php print_r($_SESSION); ?></pre>
			</div>
		</div>

	</div>

	<!-- BOOTSTRAP JS -->
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
