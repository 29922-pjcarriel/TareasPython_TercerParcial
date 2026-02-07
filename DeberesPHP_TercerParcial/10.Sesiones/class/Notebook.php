<?php

class Notebook{
	/* Atributos*/

	private $codigo;
	private $marca;
	private $precio;
	
	/*Constructor*/
	public function __construct($codigo, $marca, $precio){
		$this->codigo= $codigo;
		$this->marca= $marca;
		$this->precio = $precio;
	}
	public function getCodigo(){
		return $this->codigo;
	}
	public function getMarca(){
		return $this->marca;
	}
	public function getPrecio(){
		return $this->precio;
	}
	
}
?>