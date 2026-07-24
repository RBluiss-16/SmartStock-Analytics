import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "mysql+pymysql://root:admin@localhost:3306/proyecto"
)

tablas = [
    "categorias",
    "proveedores",
    "productos",
    "producto_categoria",
    "inventario",
    "ventas",
    "detalle_venta"
]

# 1. Vaciar las tablas manteniendo la estructura (PK, FK, AUTO_INCREMENT, etc.)
with engine.begin() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    for tabla in tablas:
        conn.execute(text(f"TRUNCATE TABLE {tabla}"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

# 2. Insertar los datos nuevos
pd.read_csv("categorias.csv").to_sql(
    "categorias", engine, if_exists="append", index=False
)

pd.read_csv("proveedores.csv").to_sql(
    "proveedores", engine, if_exists="append", index=False
)

pd.read_csv("productos.csv").to_sql(
    "productos", engine, if_exists="append", index=False
)

pd.read_csv("producto_categoria.csv").to_sql(
    "producto_categoria", engine, if_exists="append", index=False
)

pd.read_csv("inventario.csv").to_sql(
    "inventario", engine, if_exists="append", index=False
)

pd.read_csv("ventas.csv").to_sql(
    "ventas", engine, if_exists="append", index=False
)

pd.read_csv("detalle_venta.csv").to_sql(
    "detalle_venta", engine, if_exists="append", index=False
)

print("Datos reemplazados correctamente.")