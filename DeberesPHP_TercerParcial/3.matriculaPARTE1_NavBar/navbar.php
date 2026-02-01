<?php
$actual = basename($_SERVER["PHP_SELF"]);
function active($file, $actual){
  return ($file === $actual) ? "active" : "";
}
?>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container">
    <a class="navbar-brand fw-semibold" href="index.php">Matriculación</a>

    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#menu">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="menu">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item">
          <a class="nav-link <?= active('index.php', $actual) ?>" href="index.php">Vehículo</a>
        </li>
        <li class="nav-item">
          <a class="nav-link <?= active('matricula.php', $actual) ?>" href="matricula.php">Matrícula</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
