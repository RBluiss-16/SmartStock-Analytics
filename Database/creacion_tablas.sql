CREATE TABLE categorias (
    id_categoria INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255)

);

CREATE TABLE proveedores (
    id_proveedor INT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    telefono VARCHAR(50),
    correo VARCHAR(150),
    ciudad VARCHAR(100)

);

CREATE TABLE productos (
    id_producto INT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    precio NUMERIC(12,2) NOT NULL,
    id_proveedor INT NOT NULL,
    CONSTRAINT fk_producto_proveedor
        FOREIGN KEY (id_proveedor)
        REFERENCES proveedores(id_proveedor)

);

CREATE TABLE producto_categoria (
    id_producto INT NOT NULL,
    id_categoria INT NOT NULL,
    PRIMARY KEY (
        id_producto,
        id_categoria
    ),
    CONSTRAINT fk_pc_producto
        FOREIGN KEY (id_producto)
        REFERENCES productos(id_producto),

    CONSTRAINT fk_pc_categoria
        FOREIGN KEY (id_categoria)
        REFERENCES categorias(id_categoria)
);

CREATE TABLE inventario (
    id_inventario INT PRIMARY KEY,
    id_producto INT UNIQUE NOT NULL,
    cantidad_disponible INT NOT NULL,
    stock_minimo INT NOT NULL,
    ultima_actualizacion DATE,
    CONSTRAINT fk_inventario_producto
        FOREIGN KEY (id_producto)
        REFERENCES productos(id_producto)

);

CREATE TABLE ventas (
    id_venta INT PRIMARY KEY,
    fecha_venta DATE NOT NULL,
    total_venta NUMERIC(12,2) NOT NULL
);

CREATE TABLE detalle_venta (
    id_detalle INT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario NUMERIC(12,2) NOT NULL,
    subtotal NUMERIC(12,2) NOT NULL,
    CONSTRAINT fk_detalle_venta
        FOREIGN KEY (id_venta)
        REFERENCES ventas(id_venta),

    CONSTRAINT fk_detalle_producto
        FOREIGN KEY (id_producto)
        REFERENCES productos(id_producto)

);
