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
	    //echo "EJECUTANDOSE EL CONSTRUCTOR MATRICULA<br><br>";
	}


	public function get_form($id=NULL){

		if(($id == NULL) || ($id == 0) ) {

			$this->fecha = NULL;
			$this->vehiculo = NULL;
			$this->agencia = NULL;
			$this->anio = NULL;

			$op = "new";
			$bandera = 1;

		}else{

			$sql = "SELECT * FROM matricula WHERE id=$id;";
			$res = $this->con->query($sql);
			$row = $res->fetch_assoc();
            $num = $res->num_rows;
            $bandera = ($num==0) ? 0 : 1;

            if(!($bandera)){
                $mensaje = "tratar de actualizar la matricula con id= ".$id . "<br>";
                echo $this->_message_error($mensaje);

            }else{

				echo "<br>REGISTRO A MODIFICAR: <br>";
				echo "<pre>";
					print_r($row);
				echo "</pre>";

				// ATRIBUTOS DE LA CLASE MATRICULA
				$this->fecha = $row['fecha'];
				$this->vehiculo = $row['vehiculo'];
				$this->agencia = $row['agencia'];
				$this->anio = $row['anio'];

				$op = "update";
            }
		}

		if($bandera){

			$html = '
			<form name="Form_matricula" method="POST" action="index.php">

				<input type="hidden" name="id" value="' . $id  . '">
				<input type="hidden" name="op" value="' . $op  . '">

				<table border="2" align="center">
					<tr>
						<th colspan="2">DATOS MATRÍCULA</th>
					</tr>

					<tr>
						<td>Fecha:</td>
						<td><input type="date" name="fecha" value="' . $this->fecha . '"></td>
					</tr>

					<tr>
						<td>Vehículo:</td>
						<td>' . $this->_get_combo_db("vehiculo","id","placa","vehiculo",$this->vehiculo) . '</td>
					</tr>

					<tr>
						<td>Agencia:</td>
						<td>' . $this->_get_combo_db("agencia","id","descripcion","agencia",$this->agencia) . '</td>
					</tr>

					<tr>
						<td>Año:</td>
						<td>' . $this->_get_combo_anio("anio",1950,$this->anio) . '</td>
					</tr>

					<tr>
						<th colspan="2"><input type="submit" name="Guardar" value="GUARDAR"></th>
					</tr>
				</table>
			</form>';

			return $html;
		}
	}



    public function get_list(){

        $d_new = "new/0";                           
        $d_new_final = base64_encode($d_new);       

        $html = ' 
        <div class="table-responsive">
        <table class="table table-striped table-bordered table-hover text-center align-middle">
            <tr>
                <th colspan="8">Lista de Matrículas</th>
            </tr>

            <tr>
                <th colspan="8">
                    <a href="index.php?mod=matricula&d=' . $d_new_final . '">Nuevo</a>
                    <!-- NUEVO AÚN NO SE USA, PERO SE DEJA IGUAL QUE EN VEHICULO -->
                </th>
            </tr>

            <tr>
                <th>Fecha</th>
                <th>Vehículo (Placa)</th>
                <th>Agencia (Descripción)</th>
                <th>Año</th>
                <th colspan="3">Acciones</th>
            </tr>';

        $sql = "SELECT m.id, m.fecha, v.placa as vehiculo, a.descripcion as agencia, m.anio
                FROM matricula m, vehiculo v, agencia a
                WHERE m.vehiculo=v.id AND m.agencia=a.id;";

        $res = $this->con->query($sql);

        // VERIFICA si existe TUPLAS EN EJECUCION DEL Query
        $num = $res->num_rows;
        if($num != 0){

            while($row = $res->fetch_assoc()){

                // URL PARA BORRAR
                $d_del = "del/" . $row['id'];
                $d_del_final = base64_encode($d_del);

                // URL PARA ACTUALIZAR
                $d_act = "act/" . $row['id'];
                $d_act_final = base64_encode($d_act);

                // URL PARA EL DETALLE
                $d_det = "det/" . $row['id'];
                $d_det_final = base64_encode($d_det);

                $html .= '
                    <tr>
                        <td>' . $row['fecha'] . '</td>
                        <td>' . $row['vehiculo'] . '</td>
                        <td>' . $row['agencia'] . '</td>
                        <td>' . $row['anio'] . '</td>

                        <td><a href="index.php?mod=matricula&d=' . $d_del_final . '">Borrar</a></td>
                        <td><a href="index.php?mod=matricula&d=' . $d_act_final . '">Actualizar</a></td>
                        <td><a href="index.php?mod=matricula&d=' . $d_det_final . '">Detalle</a></td>
                    </tr>';
            }

        }else{
            $mensaje = "Tabla Matricula" . "<br>";
            echo $this->_message_BD_Vacia($mensaje);
            echo "<br><br><br>";
        }

        $html .= '
        </table>
        </div>';

        return $html;
    }





    public function get_detail_matricula($id){

        $sql = "SELECT m.fecha, v.placa as vehiculo, a.descripcion as agencia, m.anio
                FROM matricula m, vehiculo v, agencia a
                WHERE m.id=$id AND m.vehiculo=v.id AND m.agencia=a.id;";

        $res = $this->con->query($sql);
        $row = $res->fetch_assoc();

        $num = $res->num_rows;

        if($num == 0){

            $mensaje = "desplegar el detalle de la matricula con id= ".$id . "<br>";
            echo $this->_message_error($mensaje);

        }else{

            
            // echo "<br>TUPLA<br>";
            // echo "<pre>";
            //     print_r($row);
            // echo "</pre>";
            // ===============================

            $html = '
            <div class="row justify-content-center">
                <div class="col-md-7 col-lg-6">

                    <div class="card shadow-sm">
                        <div class="card-header bg-success text-white text-center fw-bold">
                            Detalle Matrícula
                        </div>

                        <div class="card-body p-0">
                            <table class="table table-bordered mb-0">
                                <tr>
                                    <th class="bg-light w-50">Fecha</th>
                                    <td>'. $row['fecha'] .'</td>
                                </tr>
                                <tr>
                                    <th class="bg-light">Vehículo (Placa)</th>
                                    <td>'. $row['vehiculo'] .'</td>
                                </tr>
                                <tr>
                                    <th class="bg-light">Agencia (Descripción)</th>
                                    <td>'. $row['agencia'] .'</td>
                                </tr>
                                <tr>
                                    <th class="bg-light">Año</th>
                                    <td>'. $row['anio'] .'</td>
                                </tr>
                            </table>
                        </div>

                        <div class="card-footer text-center">
                            <a href="index.php?mod=matricula" class="btn btn-secondary">
                                Regresar
                            </a>
                        </div>
                    </div>

                </div>
            </div>';

            return $html;
        }
    }




	public function delete_matricula($id){

		$sql = "DELETE FROM matricula WHERE id=$id;";
		if($this->con->query($sql)){
			echo $this->_message_ok("eliminó");
		}else{
			echo $this->_message_error("eliminar<br>");
		}
	}



//********************************************************************************************************
	/*
	 $tabla es la tabla de la base de datos
	 $valor es el nombre del campo que utilizaremos como valor del option
	 $etiqueta es nombre del campo que utilizaremos como etiqueta del option
	 $nombre es el nombre del campo tipo combo box (select)
	 * $defecto es el valor para que cargue el combo por defecto
	 */
	private function _get_combo_db($tabla,$valor,$etiqueta,$nombre,$defecto=NULL){
		$html = '<select name="' . $nombre . '">';
		$sql = "SELECT $valor,$etiqueta FROM $tabla;";
		$res = $this->con->query($sql);

		while($row = $res->fetch_assoc()){
			$html .= ($defecto == $row[$valor])
				? '<option value="' . $row[$valor] . '" selected>' . $row[$etiqueta] . '</option>' . "\n"
				: '<option value="' . $row[$valor] . '">' . $row[$etiqueta] . '</option>' . "\n";
		}
		$html .= '</select>';
		return $html;
	}


	private function _get_combo_anio($nombre,$anio_inicial,$defecto=NULL){
		$html = '<select name="' . $nombre . '">';
		$anio_actual = date('Y');
		for($i=$anio_inicial;$i<=$anio_actual;$i++){
			$html .= ($defecto == $i)
				? '<option value="' . $i . '" selected>' . $i . '</option>' . "\n"
				: '<option value="' . $i . '">' . $i . '</option>' . "\n";
		}
		$html .= '</select>';
		return $html;
	}



//***************************************************************************************************************************

	private function _message_error($tipo){
		$html = '
		<table border="0" align="center">
			<tr>
				<th>Error al ' . $tipo . 'Favor contactar a .................... </th>
			</tr>
			<tr>
				<th><a href="index.php">Regresar</a></th>
			</tr>
		</table>';
		return $html;
	}


	private function _message_BD_Vacia($tipo){
	   $html = '
		<table border="0" align="center">
			<tr>
				<th> NO existen registros en la ' . $tipo . 'Favor contactar a .................... </th>
			</tr>
		</table>';
		return $html;
	}


	private function _message_ok($tipo){
		$html = '
		<table border="0" align="center">
			<tr>
				<th>El registro se  ' . $tipo . ' correctamente</th>
			</tr>
			<tr>
				<th><a href="index.php">Regresar</a></th>
			</tr>
		</table>';
		return $html;
	}


//************************************************************************************************************************************************
}
?>
