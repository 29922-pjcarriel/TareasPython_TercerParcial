<?php
class matricula{

	private $id;
	private $fecha;
	private $vehiculo;
	private $agencia;
	private $anio;
	private $con;

	function __construct($cn){
		$this->con = $cn;
	}

	// ========================= GUARDAR =========================
	public function save_matricula(){

		$this->fecha    = $_POST['fecha'];
		$this->vehiculo = $_POST['vehiculoCMB'];
		$this->agencia  = $_POST['agenciaCMB'];
		$this->anio     = $_POST['anio'];

		$sql = "INSERT INTO matricula VALUES(
					NULL,
					'$this->fecha',
					$this->vehiculo,
					$this->agencia,
					$this->anio
				);";

		if($this->con->query($sql)){
			return $this->_message_ok("GUARDÓ");
		}else{
			return $this->_message_error("guardar<br><br>".$this->con->error);
		}
	}

	// ========================= ACTUALIZAR =========================
	public function update_matricula(){

		$this->id       = $_POST['id'];
		$this->fecha    = $_POST['fecha'];
		$this->vehiculo = $_POST['vehiculoCMB'];
		$this->agencia  = $_POST['agenciaCMB'];
		$this->anio     = $_POST['anio'];

		$sql = "UPDATE matricula SET
					fecha='$this->fecha',
					vehiculo=$this->vehiculo,
					agencia=$this->agencia,
					anio=$this->anio
				WHERE id=$this->id;";

		if($this->con->query($sql)){
			return $this->_message_ok("MODIFICÓ");
		}else{
			return $this->_message_error("modificar<br><br>".$this->con->error);
		}
	}

	// ========================= FORMULARIO =========================
	public function get_form($id=NULL){

		if($id == NULL){
			$this->fecha = NULL;
			$this->vehiculo = NULL;
			$this->agencia = NULL;
			$this->anio = NULL;
			$op = "new";
		}else{

			$sql = "SELECT * FROM matricula WHERE id=$id;";
			$res = $this->con->query($sql);

			if(!$res || $res->num_rows==0){
				return $this->_message_error("consultar matrícula");
			}

			$row = $res->fetch_assoc();
			$this->fecha = $row['fecha'];
			$this->vehiculo = $row['vehiculo'];
			$this->agencia = $row['agencia'];
			$this->anio = $row['anio'];
			$op = "update";
		}

		$html = '
		<div class="card shadow-sm">
			<div class="card-header bg-dark text-white fw-bold">DATOS MATRÍCULA</div>
			<div class="card-body">
				<form method="POST" action="index.php?mod=matricula">
					<input type="hidden" name="id" value="'.$id.'">
					<input type="hidden" name="op" value="'.$op.'">

					<div class="row g-3">
						<div class="col-md-6">
							<label class="form-label fw-semibold">Fecha</label>
							<input class="form-control" type="date" name="fecha" value="'.$this->fecha.'" required>
						</div>

						<div class="col-md-6">
							<label class="form-label fw-semibold">Año</label>
							'.$this->_get_combo_anio("anio",2000,$this->anio).'
						</div>

						<div class="col-md-6">
							<label class="form-label fw-semibold">Vehículo</label>
							'.$this->_get_combo_db("vehiculo","id","placa","vehiculoCMB",$this->vehiculo).'
						</div>

						<div class="col-md-6">
							<label class="form-label fw-semibold">Agencia</label>
							'.$this->_get_combo_db("agencia","id","descripcion","agenciaCMB",$this->agencia).'
						</div>
					</div>

					<hr class="my-4">

					<div class="d-flex justify-content-center gap-2">
						<button class="btn btn-success px-4" type="submit">GUARDAR</button>
						<a class="btn btn-secondary px-4" href="index.php?mod=matricula">REGRESAR</a>
					</div>

				</form>
			</div>
		</div>';

		return $html;
	}

	// ========================= LISTA =========================
	public function get_list(){

		$d_new = base64_encode("new/0");

		$html = '
		<div class="card shadow-sm">
			<div class="card-header d-flex justify-content-between align-items-center bg-dark text-white">
				<span class="fw-bold">LISTA DE MATRÍCULAS</span>
				<a class="btn btn-success btn-sm" href="index.php?mod=matricula&d='.$d_new.'">+ NUEVO</a>
			</div>

			<div class="card-body">
				<div class="table-responsive">
					<table class="table table-striped table-hover align-middle mb-0">
						<thead class="table-secondary">
							<tr>
								<th>Fecha</th>
								<th>Vehículo</th>
								<th>Agencia</th>
								<th>Año</th>
								<th class="text-center" colspan="3">Acciones</th>
							</tr>
						</thead>
						<tbody>';

		$sql = "SELECT m.id, m.fecha, v.placa AS vehiculo, a.descripcion AS agencia, m.anio
				FROM matricula m, vehiculo v, agencia a
				WHERE m.vehiculo=v.id AND m.agencia=a.id;";

		$res = $this->con->query($sql);

		if(!$res){
			return $this->_message_error("listar<br><br>".$this->con->error);
		}

		while($row = $res->fetch_assoc()){

			$d_del = base64_encode("del/".$row['id']);
			$d_act = base64_encode("act/".$row['id']);
			$d_det = base64_encode("det/".$row['id']);

			$html .= '
							<tr>
								<td>'.$row['fecha'].'</td>
								<td>'.$row['vehiculo'].'</td>
								<td>'.$row['agencia'].'</td>
								<td>'.$row['anio'].'</td>

								<td class="text-center">
									<a class="btn btn-outline-danger btn-sm" href="index.php?mod=matricula&d='.$d_del.'">Borrar</a>
								</td>
								<td class="text-center">
									<a class="btn btn-outline-primary btn-sm" href="index.php?mod=matricula&d='.$d_act.'">Actualizar</a>
								</td>
								<td class="text-center">
									<a class="btn btn-outline-dark btn-sm" href="index.php?mod=matricula&d='.$d_det.'">Detalle</a>
								</td>
							</tr>';
		}

		$html .= '
						</tbody>
					</table>
				</div>
			</div>
		</div>';

		return $html;
	}

	// ========================= DETALLE =========================
	public function get_detail_matricula($id){

		$sql = "SELECT m.fecha, v.placa AS vehiculo, a.descripcion AS agencia, m.anio
				FROM matricula m, vehiculo v, agencia a
				WHERE m.id=$id AND m.vehiculo=v.id AND m.agencia=a.id;";

		$res = $this->con->query($sql);

		if(!$res || $res->num_rows==0){
			return $this->_message_error("detalle");
		}

		$row = $res->fetch_assoc();

		$html = '
		<div class="card shadow-sm">
			<div class="card-header bg-dark text-white fw-bold">DETALLE MATRÍCULA</div>
			<div class="card-body">
				<div class="row g-3">
					<div class="col-md-6"><span class="fw-semibold">Fecha:</span> '.$row['fecha'].'</div>
					<div class="col-md-6"><span class="fw-semibold">Vehículo:</span> '.$row['vehiculo'].'</div>
					<div class="col-md-6"><span class="fw-semibold">Agencia:</span> '.$row['agencia'].'</div>
					<div class="col-md-6"><span class="fw-semibold">Año:</span> '.$row['anio'].'</div>
				</div>

				<hr class="my-4">

				<div class="text-center">
					<a class="btn btn-secondary px-4" href="index.php?mod=matricula">REGRESAR</a>
				</div>
			</div>
		</div>';

		return $html;
	}

	// ========================= BORRAR =========================
	public function delete_matricula($id){
		$sql = "DELETE FROM matricula WHERE id=$id;";
		if($this->con->query($sql)){
			return $this->_message_ok("ELIMINÓ");
		}else{
			return $this->_message_error("eliminar");
		}
	}

	// ========================= UTILIDADES =========================
	private function _get_combo_db($tabla,$valor,$etiqueta,$nombre,$defecto){
		$html = '<select class="form-select" name="'.$nombre.'">';
		$res = $this->con->query("SELECT $valor,$etiqueta FROM $tabla;");
		while($row = $res->fetch_assoc()){
			$html .= ($defecto==$row[$valor])
				? '<option value="'.$row[$valor].'" selected>'.$row[$etiqueta].'</option>'
				: '<option value="'.$row[$valor].'">'.$row[$etiqueta].'</option>';
		}
		return $html.'</select>';
	}

	private function _get_combo_anio($nombre,$inicio,$defecto){
		$html = '<select class="form-select" name="'.$nombre.'">';
		for($i=$inicio;$i<=date('Y');$i++){
			$html .= ($i==$defecto)
				? '<option selected>'.$i.'</option>'
				: '<option>'.$i.'</option>';
		}
		return $html.'</select>';
	}

	private function _message_error($t){
		return '
		<div class="alert alert-danger shadow-sm" role="alert">
			<div class="fw-bold mb-1">Error al '.$t.'</div>
			<hr>
			<a class="btn btn-outline-danger btn-sm" href="index.php?mod=matricula">Regresar</a>
		</div>';
	}

	private function _message_ok($t){
		return '
		<div class="alert alert-success shadow-sm" role="alert">
			<div class="fw-bold mb-1">Se '.$t.' correctamente</div>
			<hr>
			<a class="btn btn-outline-success btn-sm" href="index.php?mod=matricula">Regresar</a>
		</div>';
	}
}
?>
