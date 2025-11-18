# -*- coding: utf-8 -*-
"""Programa principal con menú interactivo"""

from inventario import Inventario

def mostrar_menu():
    print("\n" + "="*50)
    print(" SISTEMA DE INVENTARIO TEXTIL")
    print("="*50)
    print("1.  Agregar producto")
    print("2.  Listar todos los productos")
    print("3.  Buscar por tipo de tela")
    print("4.  Buscar por talla")
    print("5.  Búsqueda combinada")
    print("6.  Aumentar stock")
    print("7.  Reducir stock (venta)")
    print("8.  Productos con bajo stock")
    print("9.  Eliminar producto")
    print("10. Ver estadísticas")
    print("11. Ver resumen por telas")
    print("12. Ver resumen por tallas")
    print("13. Ver historial de movimientos")
    print("14. Crear respaldo de BD")
    print("0.  Salir")
    print("="*50)

def main():
    print(" Iniciando sistema...")
    inventario = Inventario()
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            print("\n AGREGAR PRODUCTO")
            nombre = input("Nombre del producto: ").strip()
            tipo_tela = input("Tipo de tela: ").strip()
            talla = input("Talla: ").strip()
            color = input("Color (Enter para omitir): ").strip() or "N/A"
            try:
                cantidad = int(input("Cantidad inicial: "))
                inventario.agregar_producto(nombre, tipo_tela, talla, cantidad, color)
            except ValueError:
                print("= La cantidad debe ser un número entero")
        
        elif opcion == "2":
            print("\n LISTADO COMPLETO")
            print("Ordenar por: 1)ID 2)Nombre 3)Tela 4)Talla 5)Stock")
            orden = input("Opción (Enter = nombre): ").strip()
            orden_map = {'1': 'id', '2': 'nombre', '3': 'tipo_tela', '4': 'talla', '5': 'cantidad'}
            inventario.listar_todo(orden_map.get(orden, 'nombre'))
        
        elif opcion == "3":
            print("\n BUSCAR POR TIPO DE TELA")
            tipo_tela = input("Tipo de tela: ").strip()
            inventario.buscar_por_tela(tipo_tela)
        
        elif opcion == "4":
            print("\n BUSCAR POR TALLA")
            talla = input("Talla: ").strip()
            inventario.buscar_por_talla(talla)
        
        elif opcion == "5":
            print("\n BÚSQUEDA COMBINADA")
            print("(Deje en blanco los filtros que no necesite)")
            tela = input("Tipo de tela: ").strip() or None
            talla = input("Talla: ").strip() or None
            stock = input("Stock mínimo: ").strip()
            stock = int(stock) if stock else None
            inventario.buscar_combinado(tela, talla, stock)
        
        elif opcion == "6":
            print("\n  AUMENTAR STOCK")
            try:
                id_prod = int(input("ID del producto: "))
                cantidad = int(input("Cantidad a aumentar: "))
                inventario.aumentar_stock(id_prod, cantidad)
            except ValueError:
                print(" Valores inválidos")
        
        elif opcion == "7":
            print("\n  REDUCIR STOCK (VENTA)")
            try:
                id_prod = int(input("ID del producto: "))
                cantidad = int(input("Cantidad a reducir: "))
                inventario.reducir_stock(id_prod, cantidad)
            except ValueError:
                print(" Valores inválidos")
        
        elif opcion == "8":
            print("\n  PRODUCTOS CON BAJO STOCK")
            try:
                umbral = int(input("Umbral (Enter = 10): ") or "10")
                inventario.productos_bajo_stock(umbral)
            except ValueError:
                print(" Valor inválido")
        
        elif opcion == "9":
            print("\n  ELIMINAR PRODUCTO")
            try:
                id_prod = int(input("ID del producto: "))
                confirmacion = input(f"  ¿Está seguro de eliminar el producto ID {id_prod}? (s/n): ")
                if confirmacion.lower() == 's':
                    inventario.eliminar_producto(id_prod)
                else:
                    print(" Operación cancelada")
            except ValueError:
                print(" ID inválido")
        
        elif opcion == "10":
            inventario.mostrar_estadisticas()
        
        elif opcion == "11":
            inventario.mostrar_resumen_telas()
        
        elif opcion == "12":
            inventario.mostrar_resumen_tallas()
        
        elif opcion == "13":
            print("\n HISTORIAL DE MOVIMIENTOS")
            ver_todo = input("¿Ver historial completo? (s/n, Enter = sí): ").strip().lower()
            if ver_todo == 'n':
                try:
                    id_prod = int(input("ID del producto: "))
                    inventario.mostrar_historial(producto_id=id_prod)
                except ValueError:
                    print(" ID inválido")
            else:
                inventario.mostrar_historial()
        
        elif opcion == "14":
            print("\n CREAR RESPALDO")
            inventario.bd.crear_respaldo()
        
        elif opcion == "0":
            print("\n Cerrando sistema...")
            inventario.cerrar()
            print("¡Hasta luego!")
            break
        
        else:
            print(" Opción no válida")
        
        input("\n Presione Enter para continuar...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n Error inesperado: {e}")