use bd_corporativa_simulada;

INSERT INTO Empleados (nombre, apellido_paterno, apellido_materno, fecha_nacimiento, rfc, fecha_ingreso, puesto, salario, estado, correo, telefono, domicilio) VALUES
('Luis', 'Reyes', 'Gómez', '1990-02-15', 'REGL900215XXX', '2023-01-15', 'Auxiliar Administrativo', 8500.00, 'Activo', 'luis.reyes@email.com', '5544332211', 'Calle 1 #123, CDMX'),
('Ana', 'Martínez', 'López', '1985-05-20', 'MALA850520XXX', '2023-03-01', 'Contador', 15000.00, 'Activo', 'ana.martinez@email.com', '5511223344', 'Calle 2 #456, CDMX'),
('Carlos', 'Gómez', 'Hernández', '1992-11-10', 'GOHC921110XXX', '2023-05-20', 'Vendedor', 12000.00, 'Activo', 'carlos.gomez@email.com', '5566778899', 'Calle 3 #789, CDMX'),
('Laura', 'Torres', 'Ramírez', '1988-07-05', 'TOLR880705XXX', '2023-07-10', 'Gerente de Ventas', 25000.00, 'Activo', 'laura.torres@email.com', '5533445566', 'Calle 4 #101, CDMX'),
('Ricardo', 'López', 'Sánchez', '1995-09-12', 'LOSR950912XXX', '2023-09-01', 'Recepcionista', 8000.00, 'Activo', 'ricardo.lopez@email.com', '5522113344', 'Calle 5 #202, CDMX'),
('Sofía', 'Mendoza', 'Vargas', '1991-01-05', 'MESV910105XXX', '2024-01-05', 'Supervisor de Producción', 18000.00, 'Activo', 'sofia.mendoza@email.com', '5577889900', 'Calle 6 #303, CDMX'),
('Miguel', 'Ramírez', 'Flores', '1987-02-10', 'RAFM870210XXX', '2024-02-10', 'Analista de Sistemas', 16000.00, 'Activo', 'miguel.ramirez@email.com', '5544778899', 'Calle 7 #404, CDMX'),
('Fernanda', 'Gutiérrez', 'Pérez', '1993-03-12', 'GUPF930312XXX', '2024-03-12', 'Auxiliar de Inventario', 9000.00, 'Activo', 'fernanda.gutierrez@email.com', '5511998877', 'Calle 8 #505, CDMX'),
('Javier', 'Hernández', 'Cruz', '1990-04-20', 'HECJ900420XXX', '2024-04-20', 'Asistente de Marketing', 11000.00, 'Activo', 'javier.hernandez@email.com', '5533221144', 'Calle 9 #606, CDMX'),
('Valeria', 'Santos', 'Morales', '1985-05-15', 'SOMV850515XXX', '2024-05-15', 'Director General', 50000.00, 'Activo', 'valeria.santos@email.com', '5599887766', 'Calle 10 #707, CDMX');

INSERT INTO Productos (nombre_producto, descripcion, precio_unitario, stock) VALUES
('Laptop HP 15"', 'Laptop para oficina', 15000.00, 12),
('Mouse Logitech', 'Mouse inalámbrico', 350.00, 150),
('Teclado Mecánico', 'Teclado retroiluminado', 1200.00, 80),
('Monitor LG 24"', 'Monitor LED Full HD', 4500.00, 40),
('Silla Ergonomica', 'Silla oficina con ruedas', 3200.00, 25),
('Escritorio Oficina', 'Escritorio de madera MDF', 2800.00, 15),
('Impresora HP LaserJet', 'Impresora láser multifunción', 5000.00, 10),
('Smartphone Samsung A52', 'Teléfono Android 128GB', 7000.00, 60),
('Auriculares Bluetooth', 'Auriculares inalámbricos', 950.00, 100),
('Proyector Epson', 'Proyector HD para sala de juntas', 12000.00, 8),
('Cable HDMI 2m', 'Cable de conexión HDMI', 150.00, 200),
('Router TP-Link', 'Router WiFi 5GHz', 1200.00, 50),
('Memoria USB 32GB', 'Pendrive USB 3.0', 250.00, 300),
('Carpeta Archivadora', 'Carpeta con separadores', 90.00, 500),
('Calculadora Científica', 'Calculadora para oficina', 400.00, 120);

INSERT INTO Proveedores (nombre_proveedor, rfc, contacto, telefono, correo, domicilio) VALUES
('Tecnología Global S.A. de C.V.', 'TGS990101XXX', 'Juan Pérez', '5544332211', 'juan@tecnologiaglobal.com', 'Av. Insurgentes 123, CDMX'),
('OfiPro Distribuciones', 'OPD850202YYY', 'Ana Martínez', '5511223344', 'ana@ofipro.com', 'Calle Reforma 456, CDMX'),
('Suministros del Norte', 'SDN800303ZZZ', 'Carlos Gómez', '5566778899', 'carlos@suminort.com', 'Av. Juárez 789, Monterrey'),
('Electroventas México', 'EVM950505AAA', 'Laura Torres', '5533445566', 'laura@electroventas.com', 'Calle Hidalgo 101, Guadalajara'),
('Papelería Central', 'PCE880808BBB', 'Ricardo López', '5522113344', 'ricardo@papeleriacentral.com', 'Av. Universidad 202, CDMX');

INSERT INTO Compras (id_proveedor, fecha_compra, total) VALUES
(1, '2024-01-10', 75000.00),
(2, '2024-01-15', 3200.00),
(3, '2024-02-05', 45000.00),
(4, '2024-02-20', 60000.00),
(5, '2024-03-01', 1200.00),
(1, '2024-03-10', 20000.00),
(3, '2024-03-18', 35000.00),
(2, '2024-03-25', 5000.00),
(4, '2024-04-05', 10000.00),
(5, '2024-04-12', 2000.00);

INSERT INTO Detalle_Compras (id_compra, id_producto, cantidad, precio_unitario) VALUES
(1, 1, 5, 15000.00),
(1, 4, 5, 4500.00),
(2, 2, 10, 320.00),
(3, 3, 20, 1200.00),
(3, 5, 10, 3200.00),
(4, 8, 8, 7000.00),
(4, 9, 20, 950.00),
(5, 14, 10, 120.00),
(6, 6, 5, 2800.00),
(6, 7, 3, 5000.00),
(7, 1, 2, 15000.00),
(7, 10, 2, 12000.00),
(8, 11, 15, 150.00),
(8, 12, 5, 1200.00),
(9, 4, 2, 4500.00),
(9, 3, 3, 1200.00),
(10, 14, 15, 90.00),
(10, 15, 5, 400.00);

INSERT INTO Facturas (id_cliente, fecha_factura, total, forma_pago) VALUES
(1, '2024-01-12', 34000.00, 'Transferencia'),
(2, '2024-01-20', 12000.00, 'Efectivo'),
(3, '2024-02-10', 45000.00, 'Tarjeta'),
(4, '2024-02-22', 60000.00, 'Transferencia'),
(5, '2024-03-05', 15000.00, 'Efectivo'),
(6, '2024-03-12', 22000.00, 'Tarjeta'),
(7, '2024-03-20', 18000.00, 'Transferencia'),
(8, '2024-04-01', 25000.00, 'Efectivo'),
(9, '2024-04-10', 17000.00, 'Tarjeta'),
(10, '2024-04-15', 8000.00, 'Efectivo');

INSERT INTO Detalle_Facturas (id_factura, id_producto, cantidad, precio_unitario) VALUES
(1, 1, 2, 15000.00),
(1, 2, 5, 350.00),
(2, 3, 5, 1200.00),
(2, 5, 2, 3200.00),
(3, 4, 4, 4500.00),
(3, 6, 3, 2800.00),
(4, 8, 5, 7000.00),
(4, 9, 10, 950.00),
(5, 10, 1, 12000.00),
(5, 11, 10, 150.00),
(6, 1, 1, 15000.00),
(6, 12, 2, 1200.00),
(7, 2, 10, 350.00),
(7, 3, 2, 1200.00),
(8, 4, 3, 4500.00),
(8, 5, 1, 3200.00),
(9, 6, 2, 2800.00),
(9, 7, 1, 5000.00),
(10, 14, 5, 90.00),
(10, 15, 2, 400.00);
