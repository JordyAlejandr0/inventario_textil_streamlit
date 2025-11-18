# -*- coding: utf-8 -*-
"""Gestión de base de datos SQLite para el inventario textil"""

import sqlite3
import os
from producto import Producto
from datetime import datetime

class BaseDatos:
    def __init__(self, ruta_db="datos/inventario.db"):
        """Inicializa la conexión a la base de datos"""
        self.ruta_db = ruta_db
        self._crear_directorio()
        self.conexion = None
        self.conectar()
        self._crear_tablas()
    
    def _crear_directorio(self):
        """Crea el directorio de datos si no existe"""
        directorio = os.path.dirname(self.ruta_db)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f" Directorio '{directorio}' creado")
    
    def conectar(self):
        """Establece conexión con la base de datos"""
        try:
            self.conexion = sqlite3.connect(self.ruta_db)
            self.conexion.row_factory = sqlite3.Row
            print(f" Conectado a la base de datos: {self.ruta_db}")
        except sqlite3.Error as e:
            print(f" Error al conectar a la base de datos: {e}")
            raise
    
    def _crear_tablas(self):
        """Crea las tablas necesarias si no existen"""
        cursor = self.conexion.cursor()
        
        # Tabla principal de productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo_tela TEXT NOT NULL,
                talla TEXT NOT NULL,
                cantidad INTEGER NOT NULL DEFAULT 0,
                color TEXT DEFAULT 'N/A',
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de historial de movimientos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historial_movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                tipo_movimiento TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                cantidad_anterior INTEGER,
                cantidad_nueva INTEGER,
                usuario TEXT DEFAULT 'sistema',
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        """)
        
        # Índices para optimizar búsquedas
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tipo_tela ON productos(tipo_tela)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_talla ON productos(talla)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tela_talla ON productos(tipo_tela, talla)")
        
        self.conexion.commit()
        print(" Tablas e índices creados correctamente")
    
    def agregar_producto(self, nombre, tipo_tela, talla, cantidad, color="N/A"):
        """Agrega un nuevo producto a la base de datos"""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                INSERT INTO productos (nombre, tipo_tela, talla, cantidad, color)
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, tipo_tela.lower(), talla.upper(), cantidad, color))
            
            producto_id = cursor.lastrowid
            
            cursor.execute("""
                INSERT INTO historial_movimientos 
                (producto_id, tipo_movimiento, cantidad, cantidad_nueva)
                VALUES (?, 'ALTA', ?, ?)
            """, (producto_id, cantidad, cantidad))
            
            self.conexion.commit()
            print(f" Producto agregado con ID: {producto_id}")
            return producto_id
        except sqlite3.Error as e:
            print(f" Error al agregar producto: {e}")
            self.conexion.rollback()
            return None
    
    def obtener_todos(self, ordenar_por="id"):
        """Obtiene todos los productos ordenados"""
        try:
            cursor = self.conexion.cursor()
            orden_valido = ordenar_por if ordenar_por in ['id', 'nombre', 'tipo_tela', 'talla', 'cantidad'] else 'id'
            
            cursor.execute(f"SELECT * FROM productos ORDER BY {orden_valido}")
            
            productos = []
            for fila in cursor.fetchall():
                productos.append(Producto(
                    fila['id'], fila['nombre'], fila['tipo_tela'],
                    fila['talla'], fila['cantidad'], fila['color']
                ))
            return productos
        except sqlite3.Error as e:
            print(f" Error al obtener productos: {e}")
            return []
    
    def buscar_por_id(self, producto_id):
        """Busca un producto por su ID"""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
            fila = cursor.fetchone()
            
            if fila:
                return Producto(fila['id'], fila['nombre'], fila['tipo_tela'],
                              fila['talla'], fila['cantidad'], fila['color'])
            return None
        except sqlite3.Error as e:
            print(f" Error al buscar producto: {e}")
            return None
    
    def buscar_por_tela(self, tipo_tela):
        """Busca productos por tipo de tela (ignora color)"""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                SELECT * FROM productos 
                WHERE LOWER(tipo_tela) = LOWER(?)
                ORDER BY talla, nombre
            """, (tipo_tela,))
            
            productos = []
            for fila in cursor.fetchall():
                productos.append(Producto(
                    fila['id'], fila['nombre'], fila['tipo_tela'],
                    fila['talla'], fila['cantidad'], fila['color']
                ))
            return productos
        except sqlite3.Error as e:
            print(f" Error en búsqueda por tela: {e}")
            return []
    
    def buscar_por_talla(self, talla):
        """Busca productos por talla (ignora color)"""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                SELECT * FROM productos 
                WHERE UPPER(talla) = UPPER(?)
                ORDER BY tipo_tela, nombre
            """, (talla,))
            
            productos = []
            for fila in cursor.fetchall():
                productos.append(Producto(
                    fila['id'], fila['nombre'], fila['tipo_tela'],
                    fila['talla'], fila['cantidad'], fila['color']
                ))
            return productos
        except sqlite3.Error as e:
            print(f" Error en búsqueda por talla: {e}")
            return []
    
    def buscar_combinado(self, tipo_tela=None, talla=None, stock_minimo=None):
        """Búsqueda con múltiples filtros"""
        try:
            cursor = self.conexion.cursor()
            query = "SELECT * FROM productos WHERE 1=1"
            parametros = []
            
            if tipo_tela:
                query += " AND LOWER(tipo_tela) = LOWER(?)"
                parametros.append(tipo_tela)
            
            if talla:
                query += " AND UPPER(talla) = UPPER(?)"
                parametros.append(talla)
            
            if stock_minimo is not None:
                query += " AND cantidad >= ?"
                parametros.append(stock_minimo)
            
            query += " ORDER BY nombre"
            cursor.execute(query, parametros)
            
            productos = []
            for fila in cursor.fetchall():
                productos.append(Producto(
                    fila['id'], fila['nombre'], fila['tipo_tela'],
                    fila['talla'], fila['cantidad'], fila['color']
                ))
            return productos
        except sqlite3.Error as e:
            print(f" Error en búsqueda combinada: {e}")
            return []
    
    def actualizar_stock(self, producto_id, nueva_cantidad, tipo_movimiento="AJUSTE"):
        """Actualiza el stock de un producto y registra el movimiento"""
        try:
            cursor = self.conexion.cursor()
            
            cursor.execute("SELECT cantidad FROM productos WHERE id = ?", (producto_id,))
            resultado = cursor.fetchone()
            
            if not resultado:
                print(" Producto no encontrado")
                return False
            
            cantidad_anterior = resultado['cantidad']
            diferencia = nueva_cantidad - cantidad_anterior
            
            cursor.execute("""
                UPDATE productos 
                SET cantidad = ?, fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (nueva_cantidad, producto_id))
            
            cursor.execute("""
                INSERT INTO historial_movimientos 
                (producto_id, tipo_movimiento, cantidad, cantidad_anterior, cantidad_nueva)
                VALUES (?, ?, ?, ?, ?)
            """, (producto_id, tipo_movimiento, diferencia, cantidad_anterior, nueva_cantidad))
            
            self.conexion.commit()
            print(f" Stock actualizado: {cantidad_anterior} → {nueva_cantidad}")
            return True
        except sqlite3.Error as e:
            print(f" Error al actualizar stock: {e}")
            self.conexion.rollback()
            return False
    
    def aumentar_stock(self, producto_id, cantidad):
        """Aumenta el stock de un producto"""
        producto = self.buscar_por_id(producto_id)
        if producto:
            nueva_cantidad = producto.cantidad + cantidad
            return self.actualizar_stock(producto_id, nueva_cantidad, "ENTRADA")
        return False
    
    def reducir_stock(self, producto_id, cantidad):
        """Reduce el stock de un producto"""
        producto = self.buscar_por_id(producto_id)
        if producto:
            if producto.cantidad >= cantidad:
                nueva_cantidad = producto.cantidad - cantidad
                return self.actualizar_stock(producto_id, nueva_cantidad, "SALIDA")
            else:
                print(f" Stock insuficiente. Disponible: {producto.cantidad}")
                return False
        return False
    
    def eliminar_producto(self, producto_id):
        """Elimina un producto de la base de datos"""
        try:
            cursor = self.conexion.cursor()
            
            producto = self.buscar_por_id(producto_id)
            if not producto:
                print(" Producto no encontrado")
                return False
            
            cursor.execute("DELETE FROM historial_movimientos WHERE producto_id = ?", (producto_id,))
            cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
            
            self.conexion.commit()
            print(f" Producto eliminado (ID: {producto_id})")
            return True
        except sqlite3.Error as e:
            print(f" Error al eliminar producto: {e}")
            self.conexion.rollback()
            return False
    
    def productos_bajo_stock(self, umbral=10):
        """Obtiene productos con stock bajo"""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                SELECT * FROM productos 
                WHERE cantidad <= ?
                ORDER BY cantidad ASC
            """, (umbral,))
            
            productos = []
            for fila in cursor.fetchall():
                productos.append(Producto(
                    fila['id'], fila['nombre'], fila['tipo_tela'],
                    fila['talla'], fila['cantidad'], fila['color']
                ))
            return productos
        except sqlite3.Error as e:
            print(f" Error en consulta de bajo stock: {e}")
            return []
    
    def resumen_por_tela(self):
        """Genera resumen de stock agrupado por tipo de tela"""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                SELECT tipo_tela, SUM(cantidad) as total
                FROM productos
                GROUP BY tipo_tela
                ORDER BY total DESC
            """)
            return [(fila['tipo_tela'], fila['total']) for fila in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f" Error en resumen por tela: {e}")
            return []
    
    def resumen_por_talla(self):
        """Genera resumen de stock agrupado por talla"""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                SELECT talla, SUM(cantidad) as total
                FROM productos
                GROUP BY talla
                ORDER BY talla
            """)
            return [(fila['talla'], fila['total']) for fila in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f" Error en resumen por talla: {e}")
            return []
    
    def obtener_historial(self, producto_id=None, limite=50):
        """Obtiene el historial de movimientos"""
        try:
            cursor = self.conexion.cursor()
            
            if producto_id:
                cursor.execute("""
                    SELECT h.*, p.nombre 
                    FROM historial_movimientos h
                    JOIN productos p ON h.producto_id = p.id
                    WHERE h.producto_id = ?
                    ORDER BY h.fecha DESC
                    LIMIT ?
                """, (producto_id, limite))
            else:
                cursor.execute("""
                    SELECT h.*, p.nombre 
                    FROM historial_movimientos h
                    JOIN productos p ON h.producto_id = p.id
                    ORDER BY h.fecha DESC
                    LIMIT ?
                """, (limite,))
            
            historial = []
            for fila in cursor.fetchall():
                historial.append({
                    'id': fila['id'],
                    'producto_id': fila['producto_id'],
                    'nombre': fila['nombre'],
                    'tipo_movimiento': fila['tipo_movimiento'],
                    'cantidad': fila['cantidad'],
                    'cantidad_anterior': fila['cantidad_anterior'],
                    'cantidad_nueva': fila['cantidad_nueva'],
                    'fecha': fila['fecha']
                })
            return historial
        except sqlite3.Error as e:
            print(f" Error al obtener historial: {e}")
            return []
    
    def estadisticas_generales(self):
        """Obtiene estadísticas generales del inventario"""
        try:
            cursor = self.conexion.cursor()
            stats = {}
            
            cursor.execute("SELECT COUNT(*) as total FROM productos")
            stats['total_productos'] = cursor.fetchone()['total']
            
            cursor.execute("SELECT SUM(cantidad) as total FROM productos")
            stats['total_unidades'] = cursor.fetchone()['total'] or 0
            
            cursor.execute("SELECT COUNT(DISTINCT tipo_tela) as total FROM productos")
            stats['tipos_tela'] = cursor.fetchone()['total']
            
            cursor.execute("SELECT COUNT(DISTINCT talla) as total FROM productos")
            stats['tallas'] = cursor.fetchone()['total']
            
            cursor.execute("SELECT COUNT(*) as total FROM productos WHERE cantidad = 0")
            stats['sin_stock'] = cursor.fetchone()['total']
            
            return stats
        except sqlite3.Error as e:
            print(f" Error al obtener estadísticas: {e}")
            return {}
    
    def crear_respaldo(self, ruta_respaldo=None):
        """Crea una copia de respaldo de la base de datos"""
        if not ruta_respaldo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ruta_respaldo = f"datos/respaldo_inventario_{timestamp}.db"
        
        try:
            import shutil
            shutil.copy2(self.ruta_db, ruta_respaldo)
            print(f" Respaldo creado: {ruta_respaldo}")
            return True
        except Exception as e:
            print(f" Error al crear respaldo: {e}")
            return False
    
    def cerrar(self):
        """Cierra la conexión a la base de datos"""
        if self.conexion:
            self.conexion.close()
            print(" Conexión cerrada")