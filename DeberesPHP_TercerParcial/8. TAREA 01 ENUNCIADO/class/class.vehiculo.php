<?php
class vehiculo{
	private $id;
	private $placa;
	private $marca;
	private $motor;
	private $chasis;
	private $combustible;
	private $anio;
	private $color;
	private $foto;
	private $avaluo;
	private $con;

	function __construct($cn){
		$this->con = $cn;
	}

	//*********************** 3.1 METODO update_vehiculo() **************************************************
	public function update_vehiculo(){
		$this->id = $_POST['id'];
		$this->placa = $_POST['placa'];
		$this->motor = $_POST['motor'];
		$this->chasis = $_POST['chasis'];

		$this->marca = $_POST['marcaCMB'];
		$this->anio = $_POST['anio'];
		$this->color = $_POST['colorCMB'];
		$this->combustible = $_POST['combustibleRBT'];

		$sql = "UPDATE vehiculo SET placa='$this->placa',
									marca=$this->marca,
									motor='$this->motor',
									chasis='$this->chasis',
									combustible='$this->combustible',
									anio='$this->anio',
									color=$this->color
				WHERE id=$this->id;";

		if($this->con->query($sql)){
			echo $this->_message_ok("MODIFICÓ");
		}else{
			echo $this->_message_error("al modificar<br><br>".$this->con->error);
		}
	}


	//*********************** 3.2 METODO save_vehiculo() **************************************************
	public function save_vehiculo(){

		$this->placa = $_POST['placa'];
		$this->motor = $_POST['motor'];
		$this->chasis = $_POST['chasis'];
		$this->avaluo = $_POST['avaluo'];

		$this->marca = $_POST['marcaCMB'];
		$this->anio = $_POST['anio'];
		$this->color = $_POST['colorCMB'];
		$this->combustible = $_POST['combustibleRBT'];

		// Foto
		$this->foto = $_FILES['foto']['name'];

		$path = "./imagenes/" . $this->foto;

		if(!move_uploaded_file($_FILES['foto']['tmp_name'], $path)){
			echo $this->_message_error("Cargar la imagen");
			exit;
		}

		$sql = "INSERT INTO vehiculo VALUES(NULL,
											'$this->placa',
											$this->marca,
											'$this->motor',
											'$this->chasis',
											'$this->combustible',
											'$this->anio',
											$this->color,
											'$this->foto',
											$this->avaluo);";

		if($this->con->query($sql)){
			echo $this->_message_ok("GUARDÓ");
		}else{
			echo $this->_message_error("guardar<br><br>".$this->con->error);
		}
	}


	//*********************** 3.3 METODO _get_name_File() **************************************************
	private function _get_name_file($nombre_original, $tamanio){
		$tmp = explode(".",$nombre_original);
		$numElm = count($tmp);
		$ext = $tmp[$numElm-1];
		$cadena = "";
		for($i=1;$i<=$tamanio;$i++){
			$c = rand(65,122);
			if(($c >= 91) && ($c <=96)){
				$c = NULL;
				$i--;
			}else{
				$cadena .= chr($c);
			}
		}
		return $cadena . "." . $ext;
	}


	//*************************************** PARTE I ************************************************************
	private function _get_combo_db($tabla,$valor,$etiqueta,$nombre,$defecto){
		// MISMA LÓGICA, solo agrego clases bootstrap al select
		$html = '<select class="form-select" name="' . $nombre . '">';
		$sql = "SELECT $valor,$etiqueta FROM $tabla;";
		$res = $this->con->query($sql);

		if(!$res){
			return '<b>ERROR COMBO:</b> '.$this->con->error;
		}

		while($row = $res->fetch_assoc()){
			$html .= ($defecto == $row[$valor])
				? '<option value="' . $row[$valor] . '" selected>' . $row[$etiqueta] . '</option>' . "\n"
				: '<option value="' . $row[$valor] . '">' . $row[$etiqueta] . '</option>' . "\n";
		}
		$html .= '</select>';
		return $html;
	}

	private function _get_combo_anio($nombre,$anio_inicial,$defecto){
		// MISMA LÓGICA, solo clases bootstrap
		$html = '<select class="form-select" name="' . $nombre . '">';
		$anio_actual = date('Y');
		for($i=$anio_inicial;$i<=$anio_actual;$i++){
			$html .= ($i == $defecto)
				? '<option value="' . $i . '" selected>' . $i . '</option>' . "\n"
				: '<option value="' . $i . '">' . $i . '</option>' . "\n";
		}
		$html .= '</select>';
		return $html;
	}

	private function _get_radio($arreglo,$nombre,$defecto){
		// MISMA LÓGICA, solo se cambia tabla por radios bootstrap
		$html = '<div class="d-flex flex-wrap gap-3">';

		foreach($arreglo as $etiqueta){
			$checked = "";
			if($defecto == NULL){
				$checked = "checked";
				$defecto = "__ya_seleccionado__"; // evita que todos queden checked
			}else{
				if($defecto == $etiqueta) $checked = "checked";
			}

			$html .= '
				<div class="form-check">
					<input class="form-check-input" type="radio" value="' . $etiqueta . '" name="' . $nombre . '" ' . $checked . '>
					<label class="form-check-label">' . $etiqueta . '</label>
				</div>';
		}

		$html .= '</div>';
		return $html;
	}


	//************************************* PARTE II ****************************************************
	public function get_form($id=NULL){

		if($id == NULL){
			$this->placa = NULL;
			$this->marca = NULL;
			$this->motor = NULL;
			$this->chasis = NULL;
			$this->combustible = NULL;
			$this->anio = NULL;
			$this->color = NULL;
			$this->foto = NULL;
			$this->avaluo = NULL;

			$flag = NULL;
			$op = "new";

		}else{

			$sql = "SELECT * FROM vehiculo WHERE id=$id;";
			$res = $this->con->query($sql);

			if(!$res){
				return $this->_message_error("consultar vehículo<br><br>".$this->con->error);
			}

			$row = $res->fetch_assoc();
			$num = $res->num_rows;

			if($num==0){
				$mensaje = "tratar de actualizar el vehiculo con id= ".$id;
				return $this->_message_error($mensaje);
			}else{
				$this->placa = $row['placa'];
				$this->marca = $row['marca'];
				$this->motor = $row['motor'];
				$this->chasis = $row['chasis'];
				$this->combustible = $row['combustible'];
				$this->anio = $row['anio'];
				$this->color = $row['color'];
				$this->foto = $row['foto'];
				$this->avaluo = $row['avaluo'];

				$flag = "disabled";
				$op = "update";
			}
		}

		$combustibles = ["Gasolina","Diesel","Eléctrico"];

		$html = '
		<div class="card shadow-sm">
			<div class="card-header bg-dark text-white fw-bold">DATOS VEHÍCULO</div>
			<div class="card-body">
				<form name="vehiculo" method="POST" action="index.php?mod=vehiculo" enctype="multipart/form-data">

					<input type="hidden" name="id" value="' . $id  . '">
					<input type="hidden" name="op" value="' . $op  . '">

					<div class="row g-3">

						<div class="col-md-4">
							<label class="form-label fw-semibold">Placa</label>
							<input class="form-control" type="text" name="placa" value="' . $this->placa . '" required>
						</div>

						<div class="col-md-4">
							<label class="form-label fw-semibold">Marca</label>
							' . $this->_get_combo_db("marca","id","descripcion","marcaCMB",$this->marca) . '
						</div>

						<div class="col-md-4">
							<label class="form-label fw-semibold">Año</label>
							' . $this->_get_combo_anio("anio",1980,$this->anio) . '
						</div>

						<div class="col-md-6">
							<label class="form-label fw-semibold">Motor</label>
							<input class="form-control" type="text" name="motor" value="' . $this->motor . '" required>
						</div>

						<div class="col-md-6">
							<label class="form-label fw-semibold">Chasis</label>
							<input class="form-control" type="text" name="chasis" value="' . $this->chasis . '" required>
						</div>

						<div class="col-md-6">
							<label class="form-label fw-semibold d-block">Combustible</label>
							' . $this->_get_radio($combustibles, "combustibleRBT",$this->combustible) . '
						</div>

						<div class="col-md-6">
							<label class="form-label fw-semibold">Color</label>
							' . $this->_get_combo_db("color","id","descripcion","colorCMB",$this->color) . '
						</div>

						<div class="col-md-6">
							<label class="form-label fw-semibold">Foto</label>
							<input class="form-control" type="file" name="foto" ' . $flag . '>
							<div class="form-text">Sube una imagen del vehículo.</div>
						</div>

						<div class="col-md-6">
							<label class="form-label fw-semibold">Avalúo</label>
							<input class="form-control" type="text" name="avaluo" value="' . $this->avaluo . '" ' . $flag . ' required>
						</div>

					</div>

					<hr class="my-4">

					<div class="d-flex justify-content-center gap-2">
						<button class="btn btn-success px-4" type="submit">GUARDAR</button>
						<a class="btn btn-secondary px-4" href="index.php?mod=vehiculo">REGRESAR</a>
					</div>

				</form>
			</div>
		</div>';

		return $html;
	}


	public function get_list(){
		$d_new_final = base64_encode("new/0");

		$html = '
		<div class="card shadow-sm">
			<div class="card-header d-flex justify-content-between align-items-center bg-dark text-white">
				<span class="fw-bold">LISTA DE VEHÍCULOS</span>
				<a class="btn btn-success btn-sm" href="index.php?mod=vehiculo&d=' . $d_new_final . '">
					+ NUEVO
				</a>
			</div>

			<div class="card-body">
				<div class="table-responsive">
					<table class="table table-striped table-hover align-middle mb-0">
						<thead class="table-secondary">
							<tr>
								<th>Placa</th>
								<th>Marca</th>
								<th>Color</th>
								<th>Año</th>
								<th>Avalúo</th>
								<th class="text-center" colspan="3">Acciones</th>
							</tr>
						</thead>
						<tbody>';

		$sql = "SELECT v.id, v.placa, m.descripcion as marca, c.descripcion as color, v.anio, v.avaluo
				FROM vehiculo v, color c, marca m
				WHERE v.marca=m.id AND v.color=c.id;";

		$res = $this->con->query($sql);

		if(!$res){
			return $this->_message_error("listar vehículos<br><br>".$this->con->error);
		}

		while($row = $res->fetch_assoc()){
			$d_del_final = base64_encode("del/" . $row['id']);
			$d_act_final = base64_encode("act/" . $row['id']);
			$d_det_final = base64_encode("det/" . $row['id']);

			$html .= '
							<tr>
								<td>' . $row['placa'] . '</td>
								<td>' . $row['marca'] . '</td>
								<td>' . $row['color'] . '</td>
								<td>' . $row['anio'] . '</td>
								<td>$ ' . $row['avaluo'] . '</td>

								<td class="text-center">
									<a class="btn btn-outline-danger btn-sm" href="index.php?mod=vehiculo&d=' . $d_del_final . '">Borrar</a>
								</td>
								<td class="text-center">
									<a class="btn btn-outline-primary btn-sm" href="index.php?mod=vehiculo&d=' . $d_act_final . '">Actualizar</a>
								</td>
								<td class="text-center">
									<a class="btn btn-outline-dark btn-sm" href="index.php?mod=vehiculo&d=' . $d_det_final . '">Detalle</a>
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


	public function get_detail_vehiculo($id){
		$sql = "SELECT v.placa, m.descripcion as marca, v.motor, v.chasis, v.combustible, v.anio,
					   c.descripcion as color, v.foto, v.avaluo
				FROM vehiculo v, color c, marca m
				WHERE v.id=$id AND v.marca=m.id AND v.color=c.id;";

		$res = $this->con->query($sql);

		if(!$res){
			return $this->_message_error("consultar detalle<br><br>".$this->con->error);
		}

		$row = $res->fetch_assoc();
		$num = $res->num_rows;

		if($num==0){
			$mensaje = "tratar de ver detalle del vehiculo con id= ".$id;
			return $this->_message_error($mensaje);
		}else{

			$html = '
			<div class="card shadow-sm">
				<div class="card-header bg-dark text-white fw-bold">DATOS DEL VEHÍCULO</div>
				<div class="card-body">
					<div class="row g-3">
						<div class="col-md-6"><span class="fw-semibold">Placa:</span> '. $row['placa'] .'</div>
						<div class="col-md-6"><span class="fw-semibold">Marca:</span> '. $row['marca'] .'</div>

						<div class="col-md-6"><span class="fw-semibold">Motor:</span> '. $row['motor'] .'</div>
						<div class="col-md-6"><span class="fw-semibold">Chasis:</span> '. $row['chasis'] .'</div>

						<div class="col-md-6"><span class="fw-semibold">Combustible:</span> '. $row['combustible'] .'</div>
						<div class="col-md-6"><span class="fw-semibold">Año:</span> '. $row['anio'] .'</div>

						<div class="col-md-6"><span class="fw-semibold">Color:</span> '. $row['color'] .'</div>
						<div class="col-md-6"><span class="fw-semibold">Avalúo:</span> $'. $row['avaluo'] .' USD</div>

						<div class="col-md-12"><span class="fw-semibold">Valor Matrícula:</span> $'. $this->_calculo_matricula($row['avaluo']) .' USD</div>
					</div>

					<hr class="my-4">

					<div class="text-center">
						<img class="img-fluid rounded border" src="./imagenes/' . $row['foto'] . '" style="max-width:300px;">
					</div>

					<hr class="my-4">

					<div class="text-center">
						<a class="btn btn-secondary px-4" href="index.php?mod=vehiculo">REGRESAR</a>
					</div>
				</div>
			</div>';

			return $html;
		}
	}


	public function delete_vehiculo($id){
		$sql = "DELETE FROM vehiculo WHERE id=$id;";
		if($this->con->query($sql)){
			return $this->_message_ok("ELIMINÓ");
		}else{
			return $this->_message_error("eliminar<br><br>".$this->con->error);
		}
	}


	//*************************************************************************
	private function _calculo_matricula($avaluo){
		return number_format(($avaluo * 0.10),2);
	}


	//******************* MENSAJES ******************************************************
	private function _message_error($tipo){
		$html = '
		<div class="alert alert-danger shadow-sm" role="alert">
			<div class="fw-bold mb-1">Error al ' . $tipo . '.</div>
			<div>Favor contactar a ....................</div>
			<hr>
			<a class="btn btn-outline-danger btn-sm" href="index.php?mod=vehiculo">Regresar</a>
		</div>';
		return $html;
	}

	private function _message_ok($tipo){
		$html = '
		<div class="alert alert-success shadow-sm" role="alert">
			<div class="fw-bold mb-1">El registro se ' . $tipo . ' correctamente</div>
			<hr>
			<a class="btn btn-outline-success btn-sm" href="index.php?mod=vehiculo">Regresar</a>
		</div>';
		return $html;
	}

} // FIN CLASE
?>
