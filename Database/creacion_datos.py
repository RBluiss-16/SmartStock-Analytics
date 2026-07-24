from faker import Faker
import pandas as pd
import random

fake = Faker('es_CO')

# Categorias

categorias = pd.DataFrame({
    "id_categoria": range(1, 9),
    "nombre": [
        "Tecnología",
        "Hogar",
        "Alimentos",
        "Bebidas",
        "Aseo",
        "Ropa",
        "Papelería",
        "Mascotas"
    ],
    "descripcion": [
        "Productos tecnológicos",
        "Productos para el hogar",
        "Productos alimenticios",
        "Bebidas y refrescos",
        "Productos de aseo",
        "Vestuario y accesorios",
        "Artículos de oficina",
        "Productos para mascotas"
    ]
})

# Proveedores

proveedores = []

for i in range(1, 16):

    proveedores.append({
        "id_proveedor": i,
        "nombre": fake.company(),
        "telefono": fake.phone_number(),
        "correo": fake.company_email(),
        "ciudad": fake.city()
    })

proveedores = pd.DataFrame(proveedores)

# Tipos de producto por categoria (lo que varía es el tipo base, no el nombre final)

tipos_por_categoria = {
    1: ["Mouse", "Teclado", "Monitor", "Audífonos", "Cargador", "Parlante", "Cámara", "Router", "Disco duro", "Memoria USB"],
    2: ["Lámpara", "Cortina", "Almohada", "Sábana", "Toalla", "Organizador", "Espejo", "Reloj de pared", "Tapete", "Cesto"],
    3: ["Arroz", "Pasta", "Aceite", "Harina", "Azúcar", "Café", "Chocolate", "Cereal", "Enlatado", "Galletas"],
    4: ["Gaseosa", "Jugo", "Agua", "Cerveza", "Té", "Bebida energizante", "Malteada", "Refresco"],
    5: ["Detergente", "Jabón", "Shampoo", "Desinfectante", "Suavizante", "Limpiador", "Cloro", "Esponja"],
    6: ["Camiseta", "Pantalón", "Chaqueta", "Gorra", "Medias", "Sudadera", "Vestido", "Buso"],
    7: ["Cuaderno", "Lapicero", "Carpeta", "Resma de papel", "Marcador", "Calculadora", "Agenda", "Grapadora"],
    8: ["Croquetas", "Correa", "Juguete para mascota", "Cama para mascota", "Shampoo para mascota", "Comedero", "Arena sanitaria"]
}

# Marcas / adjetivos genéricos que dan variedad sin depender de una lista temática fija

marcas_genericas = [fake.company().split()[0] for _ in range(30)]

adjetivos_genericos = ["Premium", "Clásico", "Estándar", "Especial", "Familiar", "Económico", "Extra", "Original"]

# Productos

productos = []
producto_categoria = []

for i in range(1, 101):

    id_categoria = random.choice(categorias["id_categoria"])
    tipo = random.choice(tipos_por_categoria[id_categoria])
    marca = random.choice(marcas_genericas)
    adjetivo = random.choice(adjetivos_genericos)

    nombre = f"{tipo} {marca} {adjetivo}"

    productos.append({
        "id_producto": i,
        "nombre": nombre,
        "precio": random.randint(5000, 500000),
        "id_proveedor": random.randint(1, 15)
    })

    # Categoria principal obligatoria
    producto_categoria.append({
        "id_producto": i,
        "id_categoria": id_categoria
    })

    # Posible segunda categoria (opcional, distinta a la principal)
    if random.random() < 0.3:

        otras_categorias = [c for c in categorias["id_categoria"] if c != id_categoria]
        segunda_categoria = random.choice(otras_categorias)

        producto_categoria.append({
            "id_producto": i,
            "id_categoria": segunda_categoria
        })

productos = pd.DataFrame(productos)
producto_categoria = pd.DataFrame(producto_categoria)

# Inventario

inventario = []

for producto in productos["id_producto"]:

    # 15% críticos
    if random.random() < 0.15:

        stock_minimo = random.randint(10, 30)
        cantidad = random.randint(0, stock_minimo)

    else:

        stock_minimo = random.randint(10, 30)
        cantidad = random.randint(
            stock_minimo + 1,
            stock_minimo + 150
        )

    inventario.append({
        "id_inventario": producto,
        "id_producto": producto,
        "cantidad_disponible": cantidad,
        "stock_minimo": stock_minimo,
        "ultima_actualizacion": fake.date_this_year()
    })

inventario = pd.DataFrame(inventario)

# Ventas

ventas = []

for i in range(1, 501):

    ventas.append({
        "id_venta": i,
        "fecha_venta": fake.date_between(
            start_date='-1y',
            end_date='today'
        ),
        "total_venta": 0
    })

ventas = pd.DataFrame(ventas)

# Detalle venta

detalle_venta = []

id_detalle = 1

for venta in ventas["id_venta"]:

    cantidad_productos = random.randint(1, 5)

    productos_vendidos = random.sample(
        list(productos["id_producto"]),
        cantidad_productos
    )

    total = 0

    for producto in productos_vendidos:

        precio = productos.loc[
            productos["id_producto"] == producto,
            "precio"
        ].values[0]

        cantidad = random.randint(1, 10)

        subtotal = precio * cantidad

        total += subtotal

        detalle_venta.append({
            "id_detalle": id_detalle,
            "id_venta": venta,
            "id_producto": producto,
            "cantidad": cantidad,
            "precio_unitario": precio,
            "subtotal": subtotal
        })

        id_detalle += 1

    ventas.loc[
        ventas["id_venta"] == venta,
        "total_venta"
    ] = total

detalle_venta = pd.DataFrame(detalle_venta)

# Exportación

categorias.to_csv("categorias.csv", index=False)
proveedores.to_csv("proveedores.csv", index=False)
productos.to_csv("productos.csv", index=False)
producto_categoria.to_csv("producto_categoria.csv", index=False)
inventario.to_csv("inventario.csv", index=False)
ventas.to_csv("ventas.csv", index=False)
detalle_venta.to_csv("detalle_venta.csv", index=False)

print("Archivos generados correctamente.")