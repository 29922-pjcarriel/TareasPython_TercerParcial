<html lang="es">
<head>
	<title>Formulario de login</title>
	<meta charset="utf-8">

	<!-- BOOTSTRAP CSS -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body class="bg-light">

	<div class="container vh-100 d-flex justify-content-center align-items-center">

		<div class="card shadow" style="max-width: 450px; width:100%;">
			<div class="card-body">

<?php
require("Notebook.php");
session_start();
$obj = $_SESSION['listaNote'];
			
	echo '<form action="validar.php" method="POST">';
		echo '<h3 class="text-center fw-bold mb-4">Formulario de login</h3>';

		echo '<div class="mb-3">';
			echo '<select name="usuario" class="form-select">';
				echo "<option disabled selected>" . "Escoje un usuario...." . "</option>";	
				foreach($obj as $n){
					echo "<option value=".$n->getMarca().">".$n->getMarca()."</option>";
				}
			echo "</select>";
		echo '</div>';

		echo '<div class="mb-3">';
			echo '<input type="password" class="form-control" placeholder="🔒 Contraseña" name="clave">';
		echo '</div>';

		echo '<div class="d-grid">';
			echo '<input type="submit" value="LOGIN" class="btn btn-primary">';
		echo '</div>';

	echo "</form>";
?>

			</div>
		</div>

	</div>

	<!-- BOOTSTRAP JS -->
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
