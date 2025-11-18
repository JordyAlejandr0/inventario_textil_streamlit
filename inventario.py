# -*- coding: utf-8 -*-
"""Clase Inventario que integra la base de datos"""

from base_datos import BaseDatos

class Inventario:
    def __init__(self, ruta_db="datos/inventario.db"):
        """Inicializa el inventario con conexión a base de datos"""
        self.bd = BaseDatos(ruta_db)
    
    def agregar_producto(self, nombre, tipo_tela, talla, cantidad, color="N/A"):
        """Agrega un nuevo producto"""
        if not nombre or not tipo_tela or not talla:
            print(" Todos los campos son obligatorios")
            return False
        
        if cantidad < 0:
            print(" La cantidad no puede ser negativa")
            return False
        
        return self.bd.agregar_producto(nombre, tipo_tela, talla, cantidad, color)
    
    def listar_todo(self, ordenar_por="nombre"):
        """Lista todos los productos"""
        productos = self.bd.obtener_todos(ordenar_por)
        
        if not productos:
            print(" El inventario está vacío")
            return
        
        print("\n" + "="*85)
        print(f"{'ID':3} | {'NOMBRE':20} | {'TIPO TELA':12} | {'TALLA':5} | {'COLOR':10} | {'STOCK':5}")
        print("="*85)
        for p in productos:
            print(p)
        print("="*85)
        print(f"Total de productos: {len(productos)}\n")
    
    def buscar_por_tela(self, tipo_tela):
        """Busca productos por tipo de tela"""
        resultados = self.bd.buscar_por_tela(tipo_tela)
        
        if not resultados:
            print(f"  No se encontraron productos de {tipo_tela}")
            return []
        
        print(f"\n Productos de {tipo_tela.upper()}:")
        self._mostrar_resultados(resultados)
        return resultados
    
    def buscar_por_talla(self, talla):
        """Busca productos por talla"""
        resultados = self.bd.buscar_por_talla(talla)
        
        if not resultados:
            print(f"  No se encontraron productos talla {talla}")
            return []
        
        print(f"\n Productos talla {talla.upper()}:")
        self._mostrar_resultados(resultados)
        return resultados
    
    def buscar_combinado(self, tipo_tela=None, talla=None, stock_minimo=None):
        """Búsqueda con múltiples filtros"""
        resultados = self.bd.buscar_combinado(tipo_tela, talla, stock_minimo)
        
        if not resultados:
            print("  No se encontraron productos con esos criterios")
            return []
        
        print(f"\n Resultados de búsqueda:")
        self._mostrar_resultados(resultados)
        return resultados
    
    def aumentar_stock(self, producto_id, cantidad):
        """Aumenta el stock"""
        return self.bd.aumentar_stock(producto_id, cantidad)
    
    def reducir_stock(self, producto_id, cantidad):
        """Reduce el stock"""
        return self.bd.reducir_stock(producto_id, cantidad)
    
    def eliminar_producto(self, producto_id):
        """Elimina un producto"""
        return self.bd.eliminar_producto(producto_id)
    
    def productos_bajo_stock(self, umbral=10):
        """Muestra productos con bajo stock"""
        productos = self.bd.productos_bajo_stock(umbral)
        
        if not productos:
            print(f" Todos los productos tienen stock suficiente (>{umbral})")
            return []
        
        print(f"\n  ALERTA: Productos con stock bajo (≤{umbral}):")
        self._mostrar_resultados(productos)
        return productos
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas del inventario"""
        stats = self.bd.estadisticas_generales()
        
        print("\n" + "="*50)
        print(" ESTADÍSTICAS DEL INVENTARIO")
        print("="*50)
        print(f"Total de productos registrados: {stats.get('total_productos', 0)}")
        print(f"Total de unidades en stock:     {stats.get('total_unidades', 0)}")
        print(f"Tipos de tela diferentes:       {stats.get('tipos_tela', 0)}")
        print(f"Tallas disponibles:             {stats.get('tallas', 0)}")
        print(f"Productos sin stock:            {stats.get('sin_stock', 0)}")
        print("="*50)
    
    def mostrar_resumen_telas(self):
        """Muestra resumen por tipo de tela"""
        resumen = self.bd.resumen_por_tela()
        
        print("\n Stock por Tipo de Tela:")
        print("-" * 35)
        for tela, total in resumen:
            print(f"{tela.capitalize():15} : {total:5} unidades")
    
    def mostrar_resumen_tallas(self):
        """Muestra resumen por talla"""
        resumen = self.bd.resumen_por_talla()
        
        print("\n Stock por Talla:")
        print("-" * 30)
        for talla, total in resumen:
            print(f"Talla {talla:4} : {total:5} unidades")
    
    def mostrar_historial(self, producto_id=None, limite=20):
        """Muestra historial de movimientos"""
        historial = self.bd.obtener_historial(producto_id, limite)
        
        if not historial:
            print("  No hay movimientos registrados")
            return
        
        print("\n Historial de Movimientos:")
        print("="*90)
        print(f"{'ID':4} | {'PRODUCTO':20} | {'MOVIMIENTO':10} | {'CANTIDAD':8} | {'FECHA':19}")
        print("="*90)
        for mov in historial:
            print(f"{mov['id']:4} | {mov['nombre']:20} | {mov['tipo_movimiento']:10} | "
                  f"{mov['cantidad']:+8} | {mov['fecha']}")
        print("="*90)
    
    def _mostrar_resultados(self, productos):
        """Muestra lista de productos"""
        print(f"{'ID':3} | {'NOMBRE':20} | {'TELA':12} | {'TALLA':5} | {'COLOR':10} | {'STOCK':5}")
        print("-"*75)
        for p in productos:
            print(p)
        print(f"\nTotal: {len(productos)} producto(s)")
    
    def cerrar(self):
        """Cierra la conexión a la base de datos"""
        self.bd.cerrar()