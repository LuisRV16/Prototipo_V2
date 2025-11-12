# drop schema bd_corporativa_simulada;

create schema bd_corporativa_simulada;

use bd_corporativa_simulada;
select * from postulantes;
CREATE TABLE Postulantes (
    id_postulante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50),
    fecha_nacimiento DATE NOT NULL,
    curp CHAR(18) UNIQUE NOT NULL,
    rfc CHAR(13),
    correo VARCHAR(100),
    telefono VARCHAR(15),
    domicilio VARCHAR(200),
    fecha_postulacion DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE Documentos_Postulante (
    id_documento INT AUTO_INCREMENT PRIMARY KEY,
    id_postulante INT NOT NULL,
    tipo_documento VARCHAR(50) NOT NULL,
    url_documento VARCHAR(200),
    fecha_entrega DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (id_postulante) REFERENCES Postulantes(id_postulante)
);

CREATE TABLE Empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50),
    fecha_nacimiento DATE NOT NULL,
    rfc CHAR(13) UNIQUE,
    fecha_ingreso DATE NOT NULL,
    puesto VARCHAR(50) NOT NULL,
    salario DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) DEFAULT 'Activo',
    correo VARCHAR(100),
    telefono VARCHAR(15),
    domicilio VARCHAR(200)
);

CREATE TABLE Productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre_producto VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    precio_unitario DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0
);

CREATE TABLE Proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre_proveedor VARCHAR(100) NOT NULL,
    rfc CHAR(13),
    contacto VARCHAR(100),
    telefono VARCHAR(15),
    correo VARCHAR(100),
    domicilio VARCHAR(200)
);

CREATE TABLE Compras (
    id_compra INT AUTO_INCREMENT PRIMARY KEY,
    id_proveedor INT NOT NULL,
    fecha_compra DATE DEFAULT (CURRENT_DATE),
    total DECIMAL(10,2),
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor)
);

CREATE TABLE Detalle_Compras (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_compra INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_compra) REFERENCES Compras(id_compra),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);

CREATE TABLE Facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    fecha_factura DATE DEFAULT (CURRENT_DATE),
    total DECIMAL(10,2) NOT NULL,
    forma_pago VARCHAR(50)
);

CREATE TABLE Detalle_Facturas (
    id_detalle_factura INT AUTO_INCREMENT PRIMARY KEY,
    id_factura INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_factura) REFERENCES Facturas(id_factura),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);
