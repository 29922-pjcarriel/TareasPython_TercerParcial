<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ver Notebook</title>

  <!-- Bootstrap 5 -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body class="bg-light">

<div class="container py-4">

  <div class="card shadow-sm border-0">
    <div class="card-body p-4">

      <?php
      require_once("Notebook.php");
      session_start();

      echo "<h1 class='h4 mb-3'>Datos de la Notebook</h1>";

      // OPCION 1 (MISMO CÓDIGO)
      $aux = $_SESSION['LISTA'];
      $indice = $_POST['op'];
      $obj = $aux[$indice];

      echo "<div class='alert alert-info'>";
        echo "<p class='mb-1'><strong>Marca:</strong> ".$obj->getMarca()."</p>";
        echo "<p class='mb-1'><strong>Código:</strong> ".$obj->getCodigo()."</p>";
        echo "<p class='mb-0'><strong>Precio:</strong> $ ".$obj->getPrecio()."</p>";
      echo "</div>";

      // === NO SE TOCA ===
      echo "<a href='cerrar.php' class='btn btn-danger mb-3'>Cerrar Sesión</a>";

      echo "<hr>";

      echo "<pre class='bg-body-tertiary p-3 rounded'>";
      print_r($_SESSION);
      echo "</pre>";

      echo "<pre class='bg-body-tertiary p-3 rounded'>";
      print_r($_POST);
      echo "</pre>";
      ?>

    </div>
  </div>

</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
