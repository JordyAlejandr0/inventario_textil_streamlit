# -*- coding: utf-8 -*-
"""
Interfaz Gráfica para Sistema de Inventario Textil
Usa Tkinter (incluido en Python)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from inventario import Inventario
from datetime import datetime

class InterfazInventario:
    def __init__(self, root):
        self.root = root
        self.root.title("🧵 Sistema de Inventario Textil")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Colores personalizados
        self.color_primario = "#2C3E50"
        self.color_secundario = "#3498DB"
        self.color_acento = "#E74C3C"
        self.color_exito = "#27AE60"
        self.color_fondo = "#ECF0F1"
        
        # Inicializar inventario
        self.inventario = Inventario()
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Cargar datos iniciales
        self.actualizar_tabla()
    
    def configurar_estilo(self):
        """Configura el estilo visual de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para botones
        style.configure('Primary.TButton',
                       background=self.color_secundario,
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 10, 'bold'))
        
        style.map('Primary.TButton',
                 background=[('active', '#2980B9')])
        
        # Estilo para botones de eliminar
        style.configure('Danger.TButton',
                       background=self.color_acento,
                       foreground='white',
                       borderwidth=0,
                       font=('Arial', 10, 'bold'))
        
        # Estilo para frames
        style.configure('Card.TFrame',
                       background='white',
                       relief='raised',
                       borderwidth=1)
        
        # Estilo para labels
        style.configure('Title.TLabel',
                       font=('Arial', 16, 'bold'),
                       background='white',
                       foreground=self.color_primario)
        
        style.configure('Subtitle.TLabel',
                       font=('Arial', 12, 'bold'),
                       background='white',
                       foreground=self.color_secundario)
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        # Frame principal
        self.root.configure(bg=self.color_fondo)
        
        # Header
        self.crear_header()
        
        # Container principal con notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestañas
        self.crear_pestaña_productos()
        self.crear_pestaña_busqueda()
        self.crear_pestaña_estadisticas()
        self.crear_pestaña_historial()
    
    def crear_header(self):
        """Crea el encabezado de la aplicación"""
        header = tk.Frame(self.root, bg=self.color_primario, height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Título
        titulo = tk.Label(header,
                         text="🧵 SISTEMA DE INVENTARIO TEXTIL",
                         font=('Arial', 24, 'bold'),
                         bg=self.color_primario,
                         fg='white')
        titulo.pack(side='left', padx=20, pady=20)
        
        # Fecha y hora
        self.label_fecha = tk.Label(header,
                                    text=datetime.now().strftime("%d/%m/%Y %H:%M"),
                                    font=('Arial', 12),
                                    bg=self.color_primario,
                                    fg='white')
        self.label_fecha.pack(side='right', padx=20)
        
        # Actualizar hora cada segundo
        self.actualizar_hora()
    
    def actualizar_hora(self):
        """Actualiza la hora en el header"""
        self.label_fecha.config(text=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.root.after(1000, self.actualizar_hora)
    
    # ==================== PESTAÑA: PRODUCTOS ====================
    
    def crear_pestaña_productos(self):
        """Pestaña principal para gestión de productos"""
        frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(frame, text='📦 Productos')
        
        # Panel izquierdo: Formulario
        panel_izquierdo = ttk.Frame(frame, style='Card.TFrame', width=400)
        panel_izquierdo.pack(side='left', fill='y', padx=10, pady=10)
        panel_izquierdo.pack_propagate(False)
        
        # Panel derecho: Tabla
        panel_derecho = ttk.Frame(frame, style='Card.TFrame')
        panel_derecho.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        self.crear_formulario_producto(panel_izquierdo)
        self.crear_tabla_productos(panel_derecho)
    
    def crear_formulario_producto(self, parent):
        """Formulario para agregar/editar productos"""
        # Título
        titulo = ttk.Label(parent, text="Agregar Producto", style='Title.TLabel')
        titulo.pack(pady=20)
        
        # Frame para campos
        form_frame = ttk.Frame(parent, style='Card.TFrame')
        form_frame.pack(padx=20, pady=10, fill='x')
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.entry_nombre = ttk.Entry(form_frame, width=30, font=('Arial', 10))
        self.entry_nombre.grid(row=0, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="Tipo de Tela:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        self.combo_tela = ttk.Combobox(form_frame, width=28, font=('Arial', 10),
                                       values=['algodón', 'poliéster', 'lino', 'seda', 'denim', 'lycra'])
        self.combo_tela.grid(row=1, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="Talla:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', pady=5)
        self.combo_talla = ttk.Combobox(form_frame, width=28, font=('Arial', 10),
                                        values=['XS', 'S', 'M', 'L', 'XL', 'XXL', '28', '30', '32', '34', '36'])
        self.combo_talla.grid(row=2, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="Color:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky='w', pady=5)
        self.entry_color = ttk.Entry(form_frame, width=30, font=('Arial', 10))
        self.entry_color.grid(row=3, column=1, pady=5, padx=10)
        self.entry_color.insert(0, "N/A")
        
        ttk.Label(form_frame, text="Cantidad:", font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky='w', pady=5)
        self.spinbox_cantidad = ttk.Spinbox(form_frame, from_=0, to=10000, width=28, font=('Arial', 10))
        self.spinbox_cantidad.grid(row=4, column=1, pady=5, padx=10)
        
        # Botones
        btn_frame = ttk.Frame(parent, style='Card.TFrame')
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="➕ Agregar Producto", 
                  style='Primary.TButton',
                  command=self.agregar_producto).pack(pady=5, fill='x')
        
        ttk.Button(btn_frame, text="🔄 Limpiar Campos",
                  command=self.limpiar_formulario).pack(pady=5, fill='x')
        
        # Sección de actualización de stock
        stock_frame = ttk.LabelFrame(parent, text="Actualizar Stock", padding=10)
        stock_frame.pack(padx=20, pady=20, fill='x')
        
        ttk.Label(stock_frame, text="ID Producto:", font=('Arial', 9)).grid(row=0, column=0, sticky='w', pady=5)
        self.entry_id_stock = ttk.Entry(stock_frame, width=15, font=('Arial', 9))
        self.entry_id_stock.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(stock_frame, text="Cantidad:", font=('Arial', 9)).grid(row=1, column=0, sticky='w', pady=5)
        self.entry_cantidad_stock = ttk.Entry(stock_frame, width=15, font=('Arial', 9))
        self.entry_cantidad_stock.grid(row=1, column=1, pady=5, padx=5)
        
        btn_stock_frame = ttk.Frame(stock_frame)
        btn_stock_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_stock_frame, text="⬆️ Aumentar",
                  command=self.aumentar_stock).pack(side='left', padx=5)
        
        ttk.Button(btn_stock_frame, text="⬇️ Reducir",
                  command=self.reducir_stock).pack(side='left', padx=5)
        
        ttk.Button(btn_stock_frame, text="🗑️ Eliminar",
                  style='Danger.TButton',
                  command=self.eliminar_producto).pack(side='left', padx=5)
    
    def crear_tabla_productos(self, parent):
        """Tabla para mostrar productos"""
        # Título y controles
        header_frame = ttk.Frame(parent, style='Card.TFrame')
        header_frame.pack(fill='x', pady=10)
        
        ttk.Label(header_frame, text="Lista de Productos", style='Subtitle.TLabel').pack(side='left', padx=10)
        
        ttk.Button(header_frame, text="🔄 Actualizar",
                  command=self.actualizar_tabla).pack(side='right', padx=10)
        
        # Frame para la tabla
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(table_frame)
        scroll_y.pack(side='right', fill='y')
        
        scroll_x = ttk.Scrollbar(table_frame, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')
        
        # Treeview (tabla)
        self.tabla_productos = ttk.Treeview(table_frame,
                                           columns=('ID', 'Nombre', 'Tela', 'Talla', 'Color', 'Stock'),
                                           show='headings',
                                           yscrollcommand=scroll_y.set,
                                           xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tabla_productos.yview)
        scroll_x.config(command=self.tabla_productos.xview)
        
        # Configurar columnas
        self.tabla_productos.heading('ID', text='ID')
        self.tabla_productos.heading('Nombre', text='Nombre')
        self.tabla_productos.heading('Tela', text='Tipo de Tela')
        self.tabla_productos.heading('Talla', text='Talla')
        self.tabla_productos.heading('Color', text='Color')
        self.tabla_productos.heading('Stock', text='Stock')
        
        self.tabla_productos.column('ID', width=50, anchor='center')
        self.tabla_productos.column('Nombre', width=200)
        self.tabla_productos.column('Tela', width=120)
        self.tabla_productos.column('Talla', width=80, anchor='center')
        self.tabla_productos.column('Color', width=100)
        self.tabla_productos.column('Stock', width=80, anchor='center')
        
        self.tabla_productos.pack(fill='both', expand=True)
        
        # Evento de doble clic
        self.tabla_productos.bind('<Double-1>', self.cargar_producto_seleccionado)
    
    # ==================== PESTAÑA: BÚSQUEDA ====================
    
    def crear_pestaña_busqueda(self):
        """Pestaña para búsquedas avanzadas"""
        frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(frame, text='🔍 Búsqueda')
        
        # Panel de búsqueda
        panel_busqueda = ttk.Frame(frame, style='Card.TFrame')
        panel_busqueda.pack(fill='x', padx=20, pady=20)
        
        ttk.Label(panel_busqueda, text="Búsqueda Avanzada", style='Title.TLabel').pack(pady=10)
        
        # Formulario de búsqueda
        search_form = ttk.Frame(panel_busqueda)
        search_form.pack(pady=10)
        
        # Por tela
        ttk.Label(search_form, text="Tipo de Tela:", font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=5)
        self.search_tela = ttk.Entry(search_form, width=25)
        self.search_tela.grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(search_form, text="Buscar", command=self.buscar_por_tela).grid(row=0, column=2, padx=5)
        
        # Por talla
        ttk.Label(search_form, text="Talla:", font=('Arial', 10)).grid(row=1, column=0, padx=10, pady=5)
        self.search_talla = ttk.Entry(search_form, width=25)
        self.search_talla.grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(search_form, text="Buscar", command=self.buscar_por_talla).grid(row=1, column=2, padx=5)
        
        # Stock mínimo
        ttk.Label(search_form, text="Stock Mínimo:", font=('Arial', 10)).grid(row=2, column=0, padx=10, pady=5)
        self.search_stock = ttk.Entry(search_form, width=25)
        self.search_stock.grid(row=2, column=1, padx=10, pady=5)
        ttk.Button(search_form, text="Buscar", command=self.buscar_bajo_stock).grid(row=2, column=2, padx=5)
        
        ttk.Button(panel_busqueda, text="🔄 Mostrar Todos",
                  style='Primary.TButton',
                  command=self.actualizar_tabla_busqueda).pack(pady=10)
        
        # Tabla de resultados
        self.crear_tabla_busqueda(frame)
    
    def crear_tabla_busqueda(self, parent):
        """Tabla para mostrar resultados de búsqueda"""
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scroll_y = ttk.Scrollbar(table_frame)
        scroll_y.pack(side='right', fill='y')
        
        self.tabla_busqueda = ttk.Treeview(table_frame,
                                          columns=('ID', 'Nombre', 'Tela', 'Talla', 'Color', 'Stock'),
                                          show='headings',
                                          yscrollcommand=scroll_y.set)
        
        scroll_y.config(command=self.tabla_busqueda.yview)
        
        for col in ('ID', 'Nombre', 'Tela', 'Talla', 'Color', 'Stock'):
            self.tabla_busqueda.heading(col, text=col)
        
        self.tabla_busqueda.column('ID', width=50, anchor='center')
        self.tabla_busqueda.column('Nombre', width=250)
        self.tabla_busqueda.column('Tela', width=150)
        self.tabla_busqueda.column('Talla', width=100, anchor='center')
        self.tabla_busqueda.column('Color', width=120)
        self.tabla_busqueda.column('Stock', width=100, anchor='center')
        
        self.tabla_busqueda.pack(fill='both', expand=True)
    
    # ==================== PESTAÑA: ESTADÍSTICAS ====================
    
    def crear_pestaña_estadisticas(self):
        """Pestaña para estadísticas y reportes"""
        frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(frame, text='📊 Estadísticas')
        
        # Panel superior con estadísticas generales
        stats_frame = ttk.Frame(frame, style='Card.TFrame')
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Label(stats_frame, text="Estadísticas Generales", style='Title.TLabel').pack(pady=10)
        
        # Cards de estadísticas
        cards_frame = ttk.Frame(stats_frame)
        cards_frame.pack(pady=20)
        
        self.crear_card_estadistica(cards_frame, "Total Productos", "0", 0)
        self.crear_card_estadistica(cards_frame, "Total Unidades", "0", 1)
        self.crear_card_estadistica(cards_frame, "Tipos de Tela", "0", 2)
        self.crear_card_estadistica(cards_frame, "Sin Stock", "0", 3)
        
        # Botón actualizar
        ttk.Button(stats_frame, text="🔄 Actualizar Estadísticas",
                  style='Primary.TButton',
                  command=self.actualizar_estadisticas).pack(pady=10)
        
        # Área de texto para reportes
        report_frame = ttk.LabelFrame(frame, text="Reportes Detallados", padding=10)
        report_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        btn_frame = ttk.Frame(report_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="📊 Resumen por Telas",
                  command=self.mostrar_resumen_telas).pack(side='left', padx=5)
        
        ttk.Button(btn_frame, text="📏 Resumen por Tallas",
                  command=self.mostrar_resumen_tallas).pack(side='left', padx=5)
        
        self.text_reportes = scrolledtext.ScrolledText(report_frame,
                                                       width=80,
                                                       height=15,
                                                       font=('Courier', 10))
        self.text_reportes.pack(fill='both', expand=True, pady=10)
    
    def crear_card_estadistica(self, parent, titulo, valor, columna):
        """Crea una tarjeta de estadística"""
        card = tk.Frame(parent, bg='white', relief='raised', borderwidth=2)
        card.grid(row=0, column=columna, padx=10, pady=10)
        
        tk.Label(card, text=titulo, font=('Arial', 11), bg='white', fg='#7F8C8D').pack(pady=10, padx=20)
        label_valor = tk.Label(card, text=valor, font=('Arial', 24, 'bold'), bg='white', fg=self.color_secundario)
        label_valor.pack(pady=10, padx=20)
        
        # Guardar referencia para actualizar
        if not hasattr(self, 'stat_labels'):
            self.stat_labels = {}
        self.stat_labels[titulo] = label_valor
    
    # ==================== PESTAÑA: HISTORIAL ====================
    
    def crear_pestaña_historial(self):
        """Pestaña para ver historial de movimientos"""
        frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(frame, text='📜 Historial')
        
        # Controles
        control_frame = ttk.Frame(frame, style='Card.TFrame')
        control_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Label(control_frame, text="Historial de Movimientos", style='Title.TLabel').pack(pady=10)
        
        ttk.Button(control_frame, text="🔄 Actualizar Historial",
                  style='Primary.TButton',
                  command=self.actualizar_historial).pack(pady=10)
        
        # Tabla de historial
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scroll_y = ttk.Scrollbar(table_frame)
        scroll_y.pack(side='right', fill='y')
        
        self.tabla_historial = ttk.Treeview(table_frame,
                                           columns=('ID', 'Producto', 'Movimiento', 'Cantidad', 'Fecha'),
                                           show='headings',
                                           yscrollcommand=scroll_y.set)
        
        scroll_y.config(command=self.tabla_historial.yview)
        
        self.tabla_historial.heading('ID', text='ID')
        self.tabla_historial.heading('Producto', text='Producto')
        self.tabla_historial.heading('Movimiento', text='Tipo')
        self.tabla_historial.heading('Cantidad', text='Cantidad')
        self.tabla_historial.heading('Fecha', text='Fecha')
        
        self.tabla_historial.column('ID', width=50, anchor='center')
        self.tabla_historial.column('Producto', width=250)
        self.tabla_historial.column('Movimiento', width=120, anchor='center')
        self.tabla_historial.column('Cantidad', width=100, anchor='center')
        self.tabla_historial.column('Fecha', width=180)
        
        self.tabla_historial.pack(fill='both', expand=True)
        
        # Cargar historial inicial
        self.actualizar_historial()
    
    # ==================== FUNCIONES DE PRODUCTOS ====================
    
    def agregar_producto(self):
        """Agrega un nuevo producto"""
        nombre = self.entry_nombre.get().strip()
        tela = self.combo_tela.get().strip()
        talla = self.combo_talla.get().strip()
        color = self.entry_color.get().strip()
        
        try:
            cantidad = int(self.spinbox_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero")
            return
        
        if not nombre or not tela or not talla:
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos obligatorios")
            return
        
        if self.inventario.agregar_producto(nombre, tela, talla, cantidad, color):
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.limpiar_formulario()
            self.actualizar_tabla()
            self.actualizar_estadisticas()
        else:
            messagebox.showerror("Error", "No se pudo agregar el producto")
    
    def aumentar_stock(self):
        """Aumenta el stock de un producto"""
        try:
            id_producto = int(self.entry_id_stock.get())
            cantidad = int(self.entry_cantidad_stock.get())
            
            if self.inventario.aumentar_stock(id_producto, cantidad):
                messagebox.showinfo("Éxito", "Stock aumentado correctamente")
                self.actualizar_tabla()
                self.actualizar_estadisticas()
                self.entry_id_stock.delete(0, tk.END)
                self.entry_cantidad_stock.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "ID y cantidad deben ser números enteros")
    
    def reducir_stock(self):
        """Reduce el stock de un producto"""
        try:
            id_producto = int(self.entry_id_stock.get())
            cantidad = int(self.entry_cantidad_stock.get())
            
            if self.inventario.reducir_stock(id_producto, cantidad):
                messagebox.showinfo("Éxito", "Stock reducido correctamente")
                self.actualizar_tabla()
                self.actualizar_estadisticas()
                self.entry_id_stock.delete(0, tk.END)
                self.entry_cantidad_stock.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "ID y cantidad deben ser números enteros")
    
    def eliminar_producto(self):
        """Elimina un producto"""
        try:
            id_producto = int(self.entry_id_stock.get())
            
            respuesta = messagebox.askyesno("Confirmar", 
                                           f"¿Está seguro de eliminar el producto ID {id_producto}?")
            
            if respuesta:
                if self.inventario.eliminar_producto(id_producto):
                    messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                    self.actualizar_tabla()
                    self.actualizar_estadisticas()
                    self.entry_id_stock.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.combo_tela.set('')
        self.combo_talla.set('')
        self.entry_color.delete(0, tk.END)
        self.entry_color.insert(0, "N/A")
        self.spinbox_cantidad.delete(0, tk.END)
        self.spinbox_cantidad.insert(0, "0")
    
    def cargar_producto_seleccionado(self, event):
        """Carga los datos del producto seleccionado en la tabla"""
        seleccion = self.tabla_productos.selection()
        if seleccion:
            item = self.tabla_productos.item(seleccion[0])
            valores = item['values']
            
            self.entry_id_stock.delete(0, tk.END)
            self.entry_id_stock.insert(0, valores[0])
    
    # ==================== FUNCIONES DE TABLA ====================
    
    def actualizar_tabla(self):
        """Actualiza la tabla de productos"""
        # Limpiar tabla
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
        
        # Obtener productos
        productos = self.inventario.bd.obtener_todos(ordenar_por='nombre')
        
        # Llenar tabla
        for p in productos:
            self.tabla_productos.insert('', 'end', values=(
                p.id, p.nombre, p.tipo_tela, p.talla, p.color, p.cantidad
            ))
    
    def actualizar_tabla_busqueda(self):
        """Actualiza la tabla de búsqueda con todos los productos"""
        for item in self.tabla_busqueda.get_children():
            self.tabla_busqueda.delete(item)
        
        productos = self.inventario.bd.obtener_todos()
        
        for p in productos:
            self.tabla_busqueda.insert('', 'end', values=(
                p.id, p.nombre, p.tipo_tela, p.talla, p.color, p.cantidad
            ))
    
    # ==================== FUNCIONES DE BÚSQUEDA ====================
    
    def buscar_por_tela(self):
        """Busca productos por tipo de tela"""
        tela = self.search_tela.get().strip()
        if not tela:
            messagebox.showwarning("Campo vacío", "Ingrese un tipo de tela")
            return
        
        for item in self.tabla_busqueda.get_children():
            self.tabla_busqueda.delete(item)
        
        resultados = self.inventario.bd.buscar_por_tela(tela)
        
        if resultados:
            for p in resultados:
                self.tabla_busqueda.insert('', 'end', values=(
                    p.id, p.nombre, p.tipo_tela, p.talla, p.color, p.cantidad
                ))
            messagebox.showinfo("Búsqueda", f"Se encontraron {len(resultados)} productos")
        else:
            messagebox.showinfo("Sin resultados", f"No se encontraron productos con tela '{tela}'")
    
    def buscar_por_talla(self):
        """Busca productos por talla"""
        talla = self.search_talla.get().strip()
        if not talla:
            messagebox.showwarning("Campo vacío", "Ingrese una talla")
            return
        
        for item in self.tabla_busqueda.get_children():
            self.tabla_busqueda.delete(item)
        
        resultados = self.inventario.bd.buscar_por_talla(talla)
        
        if resultados:
            for p in resultados:
                self.tabla_busqueda.insert('', 'end', values=(
                    p.id, p.nombre, p.tipo_tela, p.talla, p.color, p.cantidad
                ))
            messagebox.showinfo("Búsqueda", f"Se encontraron {len(resultados)} productos")
        else:
            messagebox.showinfo("Sin resultados", f"No se encontraron productos talla '{talla}'")
    
    def buscar_bajo_stock(self):
        """Busca productos con stock bajo"""
        try:
            stock = int(self.search_stock.get().strip())
        except ValueError:
            messagebox.showerror("Error", "El stock debe ser un número entero")
            return
        
        for item in self.tabla_busqueda.get_children():
            self.tabla_busqueda.delete(item)
        
        resultados = self.inventario.bd.productos_bajo_stock(stock)
        
        if resultados:
            for p in resultados:
                self.tabla_busqueda.insert('', 'end', values=(
                    p.id, p.nombre, p.tipo_tela, p.talla, p.color, p.cantidad
                ))
            messagebox.showwarning("Alerta", f"¡{len(resultados)} productos con stock bajo!")
        else:
            messagebox.showinfo("Stock OK", f"Todos los productos tienen stock > {stock}")
    
    # ==================== FUNCIONES DE ESTADÍSTICAS ====================
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas generales"""
        stats = self.inventario.bd.estadisticas_generales()
        
        self.stat_labels["Total Productos"].config(text=str(stats.get('total_productos', 0)))
        self.stat_labels["Total Unidades"].config(text=str(stats.get('total_unidades', 0)))
        self.stat_labels["Tipos de Tela"].config(text=str(stats.get('tipos_tela', 0)))
        self.stat_labels["Sin Stock"].config(text=str(stats.get('sin_stock', 0)))
    
    def mostrar_resumen_telas(self):
        """Muestra resumen por tipo de tela"""
        self.text_reportes.delete('1.0', tk.END)
        
        resumen = self.inventario.bd.resumen_por_tela()
        
        texto = "="*60 + "\n"
        texto += "  RESUMEN POR TIPO DE TELA\n"
        texto += "="*60 + "\n\n"
        
        if resumen:
            texto += f"{'Tipo de Tela':<30} {'Total Unidades':>20}\n"
            texto += "-"*60 + "\n"
            for tela, total in resumen:
                texto += f"{tela.capitalize():<30} {total:>20}\n"
            
            total_general = sum(t[1] for t in resumen)
            texto += "-"*60 + "\n"
            texto += f"{'TOTAL GENERAL':<30} {total_general:>20}\n"
        else:
            texto += "No hay datos disponibles\n"
        
        texto += "="*60 + "\n"
        
        self.text_reportes.insert('1.0', texto)
    
    def mostrar_resumen_tallas(self):
        """Muestra resumen por talla"""
        self.text_reportes.delete('1.0', tk.END)
        
        resumen = self.inventario.bd.resumen_por_talla()
        
        texto = "="*60 + "\n"
        texto += "  RESUMEN POR TALLA\n"
        texto += "="*60 + "\n\n"
        
        if resumen:
            texto += f"{'Talla':<30} {'Total Unidades':>20}\n"
            texto += "-"*60 + "\n"
            for talla, total in resumen:
                texto += f"{talla:<30} {total:>20}\n"
            
            total_general = sum(t[1] for t in resumen)
            texto += "-"*60 + "\n"
            texto += f"{'TOTAL GENERAL':<30} {total_general:>20}\n"
        else:
            texto += "No hay datos disponibles\n"
        
        texto += "="*60 + "\n"
        
        self.text_reportes.insert('1.0', texto)
    
    # ==================== FUNCIONES DE HISTORIAL ====================
    
    def actualizar_historial(self):
        """Actualiza la tabla de historial"""
        for item in self.tabla_historial.get_children():
            self.tabla_historial.delete(item)
        
        historial = self.inventario.bd.obtener_historial(limite=100)
        
        for mov in historial:
            self.tabla_historial.insert('', 'end', values=(
                mov['id'],
                mov['nombre'],
                mov['tipo_movimiento'],
                f"{mov['cantidad']:+d}",
                mov['fecha']
            ))
    
    def cerrar_aplicacion(self):
        """Cierra la aplicación correctamente"""
        if messagebox.askokcancel("Salir", "¿Desea cerrar la aplicación?"):
            self.inventario.cerrar()
            self.root.destroy()


# ==================== FUNCIÓN PRINCIPAL ====================

def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = InterfazInventario(root)
    
    # Cargar estadísticas iniciales
    app.actualizar_estadisticas()
    
    # Protocolo de cierre
    root.protocol("WM_DELETE_WINDOW", app.cerrar_aplicacion)
    
    # Iniciar aplicación
    root.mainloop()


if __name__ == "__main__":
    main()