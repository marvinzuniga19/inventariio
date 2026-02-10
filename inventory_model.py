import sqlite3


class InventarioModel:
    def __init__(self, db_name="inventario.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._crear_tabla()

    def _crear_tabla(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        stock_minimo INTEGER DEFAULT 10
        )
        """)
        self.conn.commit()
        
        # Add stock_minimo column if it doesn't exist (for existing databases)
        try:
            self.cursor.execute("ALTER TABLE productos ADD COLUMN stock_minimo INTEGER DEFAULT 10")
            self.conn.commit()
        except sqlite3.OperationalError:
            pass  # Column already exists

    def agregar_producto(self, nombre, cantidad, precio, stock_minimo=10):
        self.cursor.execute(
            "INSERT INTO productos (nombre, cantidad, precio, stock_minimo) VALUES (?, ?, ?, ?)",
            (nombre, cantidad, precio, stock_minimo)
        )
        self.conn.commit()

    def eliminar_producto(self, producto_id):
        self.cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        self.conn.commit()

    def actualizar_producto(self, producto_id, nombre, cantidad, precio, stock_minimo=None):
        if stock_minimo is not None:
            self.cursor.execute(
                "UPDATE productos SET nombre = ?, cantidad = ?, precio = ?, stock_minimo = ? WHERE id = ?",
                (nombre, cantidad, precio, stock_minimo, producto_id)
            )
        else:
            self.cursor.execute(
                "UPDATE productos SET nombre = ?, cantidad = ?, precio = ? WHERE id = ?",
                (nombre, cantidad, precio, producto_id)
            )
        self.conn.commit()

    def obtener_producto_por_id(self, producto_id):
        self.cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
        return self.cursor.fetchone()

    def obtener_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        return self.cursor.fetchall()

    def producto_existe(self, nombre, excluir_id=None):
        if excluir_id:
            self.cursor.execute("SELECT id FROM productos WHERE nombre = ? AND id != ?", (nombre, excluir_id))
        else:
            self.cursor.execute("SELECT id FROM productos WHERE nombre = ?", (nombre,))
        return self.cursor.fetchone() is not None

    def obtener_productos_bajo_stock(self):
        self.cursor.execute("SELECT * FROM productos WHERE cantidad <= stock_minimo")
        return self.cursor.fetchall()