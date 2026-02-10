import sqlite3


class InventarioModel:
    def __init__(self, db_name="inventario.db"):
        self.db_name = db_name
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

    def backup_database(self, backup_path):
        import shutil
        try:
            # Close current connection
            self.conn.close()
            
            # Copy database file
            shutil.copy2(self.db_name if hasattr(self, 'db_name') else "inventario.db", backup_path)
            
            # Reopen connection
            self.conn = sqlite3.connect(self.db_name if hasattr(self, 'db_name') else "inventario.db")
            self.cursor = self.conn.cursor()
            
            return True
        except Exception as e:
            # Reopen connection if it failed
            try:
                self.conn = sqlite3.connect(self.db_name if hasattr(self, 'db_name') else "inventario.db")
                self.cursor = self.conn.cursor()
            except:
                pass
            raise e

    def restore_database(self, backup_path):
        import shutil
        try:
            # Close current connection
            self.conn.close()
            
            # Copy backup file to current database
            shutil.copy2(backup_path, self.db_name if hasattr(self, 'db_name') else "inventario.db")
            
            # Reopen connection
            self.conn = sqlite3.connect(self.db_name if hasattr(self, 'db_name') else "inventario.db")
            self.cursor = self.conn.cursor()
            
            return True
        except Exception as e:
            # Reopen connection if it failed
            try:
                self.conn = sqlite3.connect(self.db_name if hasattr(self, 'db_name') else "inventario.db")
                self.cursor = self.conn.cursor()
            except:
                pass
            raise e

    def obtener_estadisticas(self):
        productos = self.obtener_productos()
        
        total_productos = len(productos)
        valor_total = sum(p[2] * p[3] for p in productos)
        bajo_stock = len(self.obtener_productos_bajo_stock())
        
        # Product statistics
        productos_sin_stock = len([p for p in productos if p[2] == 0])
        valor_promedio = valor_total / total_productos if total_productos > 0 else 0
        
        # Stock statistics
        stock_total = sum(p[2] for p in productos)
        stock_minimo_total = sum(p[4] if len(p) > 4 else 10 for p in productos)
        
        return {
            'total_productos': total_productos,
            'valor_total': valor_total,
            'bajo_stock': bajo_stock,
            'sin_stock': productos_sin_stock,
            'valor_promedio': valor_promedio,
            'stock_total': stock_total,
            'stock_minimo_total': stock_minimo_total,
            'productos_criticos': bajo_stock + productos_sin_stock
        }