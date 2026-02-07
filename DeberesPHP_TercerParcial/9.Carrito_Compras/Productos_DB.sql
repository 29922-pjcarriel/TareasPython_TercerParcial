/* ==========================
   MySQL - Productos_BD
   ========================== */

-- (Opcional) crear desde cero
DROP DATABASE IF EXISTS Productos_BD;
CREATE DATABASE Productos_BD
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

USE Productos_BD;

-- Recomendado para crear tablas con FK en orden
SET FOREIGN_KEY_CHECKS = 0;

/* ==========================
   TABLA: Clientes
   ========================== */
CREATE TABLE Clientes (
  ClienteID INT NOT NULL AUTO_INCREMENT,
  RazonSocial   VARCHAR(50)  NULL,
  Direccion     VARCHAR(100) NULL,
  Ciudad        VARCHAR(50)  NULL,
  Estado        VARCHAR(50)  NULL,
  CodigoPostal  VARCHAR(10)  NULL,
  Rif           VARCHAR(15)  NULL,
  Pais          VARCHAR(50)  NULL,
  Telefonos     VARCHAR(50)  NULL,
  PRIMARY KEY (ClienteID)
) ENGINE=InnoDB;

/* ==========================
   TABLA: Productos
   ========================== */
CREATE TABLE Productos (
  ProductoID INT NOT NULL AUTO_INCREMENT,
  Descripcion VARCHAR(200) NOT NULL,
  Precio DECIMAL(18,2) NOT NULL,
  Imagen LONGTEXT NOT NULL,     -- nvarchar(max) -> LONGTEXT
  Detalles VARCHAR(50) NOT NULL,
  PRIMARY KEY (ProductoID)
) ENGINE=InnoDB;

/* ==========================
   TABLA: Pedidos
   ========================== */
CREATE TABLE Pedidos (
  PedidoID INT NOT NULL AUTO_INCREMENT,
  ClienteID INT NULL,
  FechaPedido DATETIME NULL,
  PRIMARY KEY (PedidoID),
  INDEX idx_pedidos_clienteid (ClienteID),
  CONSTRAINT FK_Pedidos_Clientes
    FOREIGN KEY (ClienteID)
    REFERENCES Clientes(ClienteID)
    ON UPDATE RESTRICT
    ON DELETE RESTRICT
) ENGINE=InnoDB;

/* ==========================
   TABLA: PedidosItems
   ========================== */
CREATE TABLE PedidosItems (
  PedidoItemID INT NOT NULL AUTO_INCREMENT,
  PedidoID INT NOT NULL,
  ProductoID INT NOT NULL,
  Cantidad INT NOT NULL,
  PRIMARY KEY (PedidoItemID),
  INDEX idx_items_pedidoid (PedidoID),
  INDEX idx_items_productoid (ProductoID),
  CONSTRAINT FK_PedidosItems_Pedidos
    FOREIGN KEY (PedidoID)
    REFERENCES Pedidos(PedidoID)
    ON UPDATE RESTRICT
    ON DELETE RESTRICT,
  CONSTRAINT FK_PedidosItems_Productos
    FOREIGN KEY (ProductoID)
    REFERENCES Productos(ProductoID)
    ON UPDATE RESTRICT
    ON DELETE RESTRICT
) ENGINE=InnoDB;

SET FOREIGN_KEY_CHECKS = 1;


USE Productos_BD;

-- =========================
-- 1) CLIENTES (2)
-- =========================
INSERT INTO Clientes (RazonSocial, Direccion, Ciudad, Estado, CodigoPostal, Rif, Pais, Telefonos) VALUES
('Comercial Tapia S.A.', 'Av. 6 de Diciembre y Portugal', 'Quito', 'Pichincha', '170135', 'J-0912345678-1', 'Ecuador', '0991112233 / 022345678');

INSERT INTO Clientes (RazonSocial, Direccion, Ciudad, Estado, CodigoPostal, Rif, Pais, Telefonos) VALUES
('Distribuidora Guayas Cía. Ltda.', 'Av. Francisco de Orellana', 'Guayaquil', 'Guayas', '090112', 'J-0998765432-0', 'Ecuador', '0982223344 / 042123456');


-- =========================
-- 2) PRODUCTOS (6)
-- =========================
INSERT INTO Productos (Descripcion, Precio, Imagen, Detalles) VALUES
('Mouse Gamer RGB', 15.50, 'mouse.jpg', 'USB 12000 DPI');

INSERT INTO Productos (Descripcion, Precio, Imagen, Detalles) VALUES
('Teclado Mecánico', 45.00, 'teclado.jpg', 'Switch Blue');

INSERT INTO Productos (Descripcion, Precio, Imagen, Detalles) VALUES
('Audífonos Bluetooth', 22.99, 'audifonos.jpg', 'Batería 8h');

INSERT INTO Productos (Descripcion, Precio, Imagen, Detalles) VALUES
('Pad Mouse XL', 8.75, 'pad.jpg', 'Antideslizante');

INSERT INTO Productos (Descripcion, Precio, Imagen, Detalles) VALUES
('Webcam Full HD', 29.90, 'webcam.jpg', '1080p Mic');

INSERT INTO Productos (Descripcion, Precio, Imagen, Detalles) VALUES
('Memoria USB 64GB', 10.25, 'usb64.jpg', 'USB 3.0');


-- =========================
-- 3) PEDIDOS (2)
-- =========================
INSERT INTO Pedidos (ClienteID, FechaPedido) VALUES
(1, '2026-01-20 10:15:00');

INSERT INTO Pedidos (ClienteID, FechaPedido) VALUES
(2, '2026-01-21 16:40:00');


-- =========================
-- 4) PEDIDOSITEMS (7)
--    Pedido 1 (4 items) y Pedido 2 (3 items)
-- =========================
-- PedidoID = 1 (Cliente 1)
INSERT INTO PedidosItems (PedidoID, ProductoID, Cantidad) VALUES (1, 1, 2);  -- 2 Mouse
INSERT INTO PedidosItems (PedidoID, ProductoID, Cantidad) VALUES (1, 4, 1);  -- 1 Pad
INSERT INTO PedidosItems (PedidoID, ProductoID, Cantidad) VALUES (1, 6, 3);  -- 3 USB 64GB
INSERT INTO PedidosItems (PedidoID, ProductoID, Cantidad) VALUES (1, 5, 1);  -- 1 Webcam

-- PedidoID = 2 (Cliente 2)
INSERT INTO PedidosItems (PedidoID, ProductoID, Cantidad) VALUES (2, 2, 2);  -- 2 Teclado
INSERT INTO PedidosItems (PedidoID, ProductoID, Cantidad) VALUES (2, 3, 2);  -- 2 Audífonos
INSERT INTO PedidosItems (PedidoID, ProductoID, Cantidad) VALUES (2, 1, 1);  -- 1 Mouse
