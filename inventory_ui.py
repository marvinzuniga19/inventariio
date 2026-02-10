import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
from inventory_model import InventarioModel
import csv
from datetime import datetime
import os


class InventarioUI:
    def __init__(self, controller=None):
        self.controller = controller
        self.model = controller.model if controller else InventarioModel()
        self.app = tb.Window(themename="superhero")
        self.app.title("Gestor de Inventario")
        self.app.geometry("700x500")
        self.editando_id = None
        self._crear_ui()
        self.cargar_productos()
        self.actualizar_estadisticas()
        self.configurar_atajos()
        self.verificar_alertas_inicio()
        self.app.mainloop()
    
    def run(self):
        """Run the application."""
        self.app.mainloop()

    def _crear_ui(self):
        frame_form = tb.Frame(self.app, padding=10)
        frame_form.pack(fill=X)

        self.entry_nombre = tb.Entry(frame_form)
        self.entry_cantidad = tb.Entry(frame_form)
        self.entry_precio = tb.Entry(frame_form)
        self.entry_stock_minimo = tb.Entry(frame_form, width=10)

        labels = ["Producto", "Cantidad", "Precio", "Stock Mínimo"]
        entries = [self.entry_nombre, self.entry_cantidad, self.entry_precio, self.entry_stock_minimo]

        for i, text in enumerate(labels):
            label = tb.Label(frame_form, text=text)
            label.grid(row=0, column=i, padx=5)
            entries[i].grid(row=1, column=i, padx=5)
            
            # Add tooltips
            if text == "Producto":
                self.create_tooltip(entries[i], "Nombre del producto (único)")
            elif text == "Cantidad":
                self.create_tooltip(entries[i], "Cantidad en stock (número entero)")
            elif text == "Precio":
                self.create_tooltip(entries[i], "Precio por unidad (decimal)")
            elif text == "Stock Mínimo":
                self.create_tooltip(entries[i], "Alerta cuando el stock sea igual o menor")

        self.btn_agregar = tb.Button(frame_form, text="➕ Agregar", bootstyle=SUCCESS, command=self.agregar_producto)
        self.btn_agregar.grid(row=1, column=3, padx=10)
        self.create_tooltip(self.btn_agregar, "Agregar nuevo producto (Ctrl+N)")
        
        self.btn_editar = tb.Button(frame_form, text="✏️ Editar", bootstyle=INFO, command=self.editar_producto)
        self.btn_editar.grid(row=1, column=4, padx=10)
        self.create_tooltip(self.btn_editar, "Editar producto seleccionado")
        
        self.btn_eliminar = tb.Button(frame_form, text="🗑️ Eliminar", bootstyle=DANGER, command=self.eliminar_producto)
        self.btn_eliminar.grid(row=1, column=5, padx=10)
        self.create_tooltip(self.btn_eliminar, "Eliminar producto seleccionado (Delete)")
        
        self.btn_exportar = tb.Button(frame_form, text="📄 Exportar", bootstyle=PRIMARY, command=self.exportar_csv)
        self.btn_exportar.grid(row=1, column=6, padx=10)
        self.create_tooltip(self.btn_exportar, "Exportar inventario a CSV")
        
        self.btn_alertas = tb.Button(frame_form, text="⚠️ Alertas", bootstyle=WARNING, command=self.mostrar_alertas_stock)
        self.btn_alertas.grid(row=1, column=7, padx=10)
        self.create_tooltip(self.btn_alertas, "Ver productos con stock bajo")
        
        self.btn_estadisticas = tb.Button(frame_form, text="📊 Estadísticas", bootstyle=INFO, command=self.mostrar_estadisticas)
        self.btn_estadisticas.grid(row=1, column=8, padx=10)
        self.create_tooltip(self.btn_estadisticas, "Ver estadísticas del inventario")
        
        self.btn_pdf = tb.Button(frame_form, text="📑 PDF", bootstyle=SECONDARY, command=self.generar_pdf)
        self.btn_pdf.grid(row=1, column=9, padx=10)
        self.create_tooltip(self.btn_pdf, "Generar reporte PDF")
        
        self.btn_backup = tb.Button(frame_form, text="💾 Backup", bootstyle=PRIMARY, command=self.backup_database)
        self.btn_backup.grid(row=1, column=10, padx=10)
        self.create_tooltip(self.btn_backup, "Crear copia de seguridad")
        
        self.btn_restore = tb.Button(frame_form, text="🔄 Restore", bootstyle=WARNING, command=self.restore_database)
        self.btn_restore.grid(row=1, column=11, padx=10)
        self.create_tooltip(self.btn_restore, "Restaurar desde copia")

        frame_search = tb.Frame(self.app, padding=10)
        frame_search.pack(fill=X)
        
        tb.Label(frame_search, text="🔍 Buscar:").pack(side=LEFT, padx=5)
        self.entry_busqueda = tb.Entry(frame_search)
        self.entry_busqueda.pack(side=LEFT, fill=X, expand=True, padx=5)
        self.entry_busqueda.bind("<KeyRelease>", self.filtrar_productos)
        self.create_tooltip(self.entry_busqueda, "Buscar productos (Ctrl+F)")
        
        btn_limpiar = tb.Button(frame_search, text="🧹 Limpiar", bootstyle=SECONDARY, command=self.limpiar_busqueda)
        btn_limpiar.pack(side=LEFT, padx=5)
        self.create_tooltip(btn_limpiar, "Limpiar búsqueda (Escape)")

        # Statistics panel
        frame_stats = tb.Frame(self.app, padding=10)
        frame_stats.pack(fill=X)
        
        self.stats_frame = frame_stats
        self.actualizar_estadisticas()

        frame_tabla = tb.Frame(self.app, padding=10)
        frame_tabla.pack(fill=BOTH, expand=True)

        self.tabla = tb.Treeview(frame_tabla, columns=("ID", "Producto", "Cantidad", "Precio", "Stock Mínimo"), show="headings")
        for col in ("ID", "Producto", "Cantidad", "Precio", "Stock Mínimo"):
            self.tabla.heading(col, text=col, command=lambda c=col: self.ordenar_columna(c))
            if col == "ID":
                self.tabla.column(col, anchor=CENTER, width=0, stretch=False)
            else:
                self.tabla.column(col, anchor=CENTER)
        self.tabla.pack(fill=BOTH, expand=True)
        
        # Bind right-click for context menu
        self.tabla.bind("<Button-3>", self.mostrar_menu_contextual)

    def agregar_producto(self):
        nombre = self.entry_nombre.get()
        cantidad = self.entry_cantidad.get()
        precio = self.entry_precio.get()
        stock_minimo = self.entry_stock_minimo.get()

        if not nombre or not cantidad or not precio:
            messagebox.showwarning("Error", "Los campos Producto, Cantidad y Precio son obligatorios")
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
            stock_minimo = int(stock_minimo) if stock_minimo else 10
        except ValueError:
            messagebox.showwarning("Error", "Cantidad y Stock Mínimo deben ser números enteros, precio debe ser decimal")
            return

        if self.model.producto_existe(nombre):
            messagebox.showwarning("Error", f"El producto '{nombre}' ya existe")
            return

        self.model.agregar_producto(nombre, cantidad, precio, stock_minimo)
        self.limpiar_campos()
        self.cargar_productos()
        self.actualizar_estadisticas()

    def editar_producto(self):
        seleccionado = self.tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Error", "Seleccione un producto para editar")
            return

        item = self.tabla.item(seleccionado)
        producto_id = item['values'][0]
        producto = self.model.obtener_producto_por_id(producto_id)
        
        if producto:
            self.editando_id = producto_id
            self.entry_nombre.delete(0, "end")
            self.entry_nombre.insert(0, producto[1])
            self.entry_cantidad.delete(0, "end")
            self.entry_cantidad.insert(0, str(producto[2]))
            self.entry_precio.delete(0, "end")
            self.entry_precio.insert(0, str(producto[3]))
            self.entry_stock_minimo.delete(0, "end")
            stock_minimo = str(producto[4]) if len(producto) > 4 else "10"
            self.entry_stock_minimo.insert(0, stock_minimo)
            
            # Cambiar texto del botón de agregar a "Actualizar"
            self.btn_agregar.config(text="💾 Actualizar", bootstyle=WARNING, command=self.actualizar_producto)
            self.create_tooltip(self.btn_agregar, "Actualizar producto (Enter)")

    def actualizar_producto(self):
        nombre = self.entry_nombre.get()
        cantidad = self.entry_cantidad.get()
        precio = self.entry_precio.get()
        stock_minimo = self.entry_stock_minimo.get()

        if not nombre or not cantidad or not precio:
            messagebox.showwarning("Error", "Los campos Producto, Cantidad y Precio son obligatorios")
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
            stock_minimo = int(stock_minimo) if stock_minimo else 10
        except ValueError:
            messagebox.showwarning("Error", "Cantidad y Stock Mínimo deben ser números enteros, precio debe ser decimal")
            return

        if self.model.producto_existe(nombre, self.editando_id):
            messagebox.showwarning("Error", f"El producto '{nombre}' ya existe")
            return

        self.model.actualizar_producto(self.editando_id, nombre, cantidad, precio, stock_minimo)
        self.limpiar_campos()
        self.cargar_productos()
        self.actualizar_estadisticas()
        self.restaurar_boton_agregar()

    def restaurar_boton_agregar(self):
        self.editando_id = None
        self.btn_agregar.config(text="➕ Agregar", bootstyle=SUCCESS, command=self.agregar_producto)
        self.create_tooltip(self.btn_agregar, "Agregar nuevo producto (Ctrl+N)")

    def create_tooltip(self, widget, text):
        def on_enter(event):
            tooltip = tb.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tb.Label(tooltip, text=text, background="lightyellow", relief="solid", borderwidth=1)
            label.pack()
            widget.tooltip = tooltip

        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def eliminar_producto(self):
        seleccionado = self.tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Error", "Seleccione un producto para eliminar")
            return

        item = self.tabla.item(seleccionado)
        producto_id = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto ID: {producto_id}?"):
            self.model.eliminar_producto(producto_id)
            self.cargar_productos()
            self.actualizar_estadisticas()

    def limpiar_campos(self):
        self.entry_nombre.delete(0, "end")
        self.entry_cantidad.delete(0, "end")
        self.entry_precio.delete(0, "end")
        self.entry_stock_minimo.delete(0, "end")
        if self.editando_id:
            self.restaurar_boton_agregar()

    def cargar_productos(self, filtro=""):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        productos = self.model.obtener_productos()
        
        if filtro:
            productos = [p for p in productos if filtro.lower() in str(p[1]).lower()]
        
        for producto in productos:
            item_id = self.tabla.insert("", "end", values=producto)
            
            # Add visual indicators for low stock
            if len(producto) >= 3 and producto[2] <= (producto[4] if len(producto) > 4 else 10):
                self.tabla.item(item_id, tags=("bajo_stock",))
        
        # Configure tag colors for low stock
        self.tabla.tag_configure("bajo_stock", background="#ffcccc")

    def filtrar_productos(self, event=None):
        texto_busqueda = self.entry_busqueda.get()
        self.cargar_productos(texto_busqueda)

    def limpiar_busqueda(self):
        self.entry_busqueda.delete(0, "end")
        self.cargar_productos()

    def configurar_atajos(self):
        self.app.bind("<Control-n>", lambda e: self.nuevo_producto())
        self.app.bind("<Control-N>", lambda e: self.nuevo_producto())
        self.app.bind("<Delete>", lambda e: self.eliminar_producto())
        self.app.bind("<Control-f>", lambda e: self.foco_busqueda())
        self.app.bind("<Control-F>", lambda e: self.foco_busqueda())
        self.app.bind("<Return>", lambda e: self.guardar_producto())
        self.app.bind("<Escape>", lambda e: self.cancelar_edicion())

    def nuevo_producto(self):
        self.limpiar_campos()
        self.entry_nombre.focus()

    def foco_busqueda(self):
        self.entry_busqueda.focus()
        self.entry_busqueda.select_range(0, "end")

    def guardar_producto(self):
        if self.editando_id:
            self.actualizar_producto()
        else:
            self.agregar_producto()

    def cancelar_edicion(self):
        if self.editando_id:
            self.restaurar_boton_agregar()
        self.limpiar_campos()

    def ordenar_columna(self, columna):
        productos = self.model.obtener_productos()
        
        # Get column index
        columnas = ["ID", "Producto", "Cantidad", "Precio", "Stock Mínimo"]
        col_idx = columnas.index(columna)
        
        # Sort products
        productos.sort(key=lambda x: x[col_idx] if x[col_idx] is not None else "")
        
        # Reload table
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        for producto in productos:
            item_id = self.tabla.insert("", "end", values=producto)
            
            # Add visual indicators for low stock
            if len(producto) >= 3 and producto[2] <= (producto[4] if len(producto) > 4 else 10):
                self.tabla.item(item_id, tags=("bajo_stock",))

    def mostrar_menu_contextual(self, event):
        seleccionado = self.tabla.identify_row(event.y)
        if seleccionado:
            self.tabla.selection_set(seleccionado)
            
            menu = tb.Menu(self.app, tearoff=0)
            menu.add_command(label="Editar", command=self.editar_producto)
            menu.add_command(label="Eliminar", command=self.eliminar_producto)
            menu.add_separator()
            menu.add_command(label="Copiar nombre", command=lambda: self.copiar_nombre(seleccionado))
            menu.add_command(label="Ver detalles", command=lambda: self.ver_detalles(seleccionado))
            
            menu.post(event.x_root, event.y_root)

    def copiar_nombre(self, item_id):
        item = self.tabla.item(item_id)
        nombre = item['values'][1]
        self.app.clipboard_clear()
        self.app.clipboard_append(nombre)
        messagebox.showinfo("Copiado", f"Nombre '{nombre}' copiado al portapapeles")

    def ver_detalles(self, item_id):
        item = self.tabla.item(item_id)
        producto_id = item['values'][0]
        producto = self.model.obtener_producto_por_id(producto_id)
        
        if producto:
            stock_minimo = producto[4] if len(producto) > 4 else 10
            estado = "BAJO STOCK" if producto[2] <= stock_minimo else "OK"
            color = "rojo" if producto[2] <= stock_minimo else "verde"
            
            detalles = f"""
ID: {producto[0]}
Producto: {producto[1]}
Cantidad: {producto[2]}
Precio: ${producto[3]:.2f}
Stock Mínimo: {stock_minimo}
Estado: {estado}
Valor Total: ${producto[2] * producto[3]:.2f}
            """
            
            messagebox.showinfo("Detalles del Producto", detalles.strip())

    def mostrar_alertas_stock(self):
        productos_bajo_stock = self.model.obtener_productos_bajo_stock()
        
        if not productos_bajo_stock:
            messagebox.showinfo("Alertas de Stock", "✅ No hay productos con stock bajo")
            return
        
        mensaje = "⚠️ Productos con stock bajo:\n\n"
        for producto in productos_bajo_stock:
            stock_minimo = producto[4] if len(producto) > 4 else 10
            mensaje += f"• {producto[1]}: {producto[2]} unidades (Mínimo: {stock_minimo})\n"
        
        mensaje += f"\nTotal: {len(productos_bajo_stock)} productos necesitan reabastecimiento"
        
        messagebox.showwarning("Alertas de Stock", mensaje)

    def actualizar_estadisticas(self):
        # Clear existing stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        stats = self.model.obtener_estadisticas()
        
        # Create stat labels
        stats_data = [
            ("📦 Total Productos", stats['total_productos'], "primary"),
            ("💰 Valor Total", f"${stats['valor_total']:,.2f}", "success"),
            ("⚠️ Stock Bajo", stats['bajo_stock'], "warning" if stats['bajo_stock'] > 0 else "success"),
            ("🚫 Sin Stock", stats['sin_stock'], "danger" if stats['sin_stock'] > 0 else "success")
        ]
        
        for i, (label, value, style) in enumerate(stats_data):
            frame = tb.Frame(self.stats_frame)
            frame.pack(side=LEFT, padx=10, expand=True, fill=X)
            
            tb.Label(frame, text=label, font=("Arial", 9)).pack()
            value_label = tb.Label(frame, text=str(value), font=("Arial", 12, "bold"), bootstyle=style)
            value_label.pack()

    def mostrar_estadisticas(self):
        stats = self.model.obtener_estadisticas()
        
        mensaje = f"""
📊 ESTADÍSTICAS DEL INVENTARIO

📦 Total de Productos: {stats['total_productos']}
💰 Valor Total del Inventario: ${stats['valor_total']:,.2f}
💰 Valor Promedio por Producto: ${stats['valor_promedio']:,.2f}

📈 ESTADO DE STOCK
⚠️ Productos con Stock Bajo: {stats['bajo_stock']}
🚫 Productos sin Stock: {stats['sin_stock']}
🔴 Productos Críticos (Bajo + Sin Stock): {stats['productos_criticos']}

📊 STOCK TOTAL
📦 Unidades Totales en Stock: {stats['stock_total']}
🎯 Stock Mínimo Requerido: {stats['stock_minimo_total']}
📈 Porcentaje de Stock Cubierto: {(stats['stock_total']/stats['stock_minimo_total']*100):.1f}%
        """
        
        messagebox.showinfo("Estadísticas del Inventario", mensaje.strip())

    def verificar_alertas_inicio(self):
        stats = self.model.obtener_estadisticas()
        productos_criticos = stats['productos_criticos']
        
        if productos_criticos > 0:
            productos_bajo_stock = self.model.obtener_productos_bajo_stock()
            
            mensaje = f"⚠️ ALERTAS DE INVENTARIO AL INICIAR\n\n"
            mensaje += f"📦 Productos con atención requerida: {productos_criticos}\n"
            mensaje += f"⚠️ Stock bajo: {stats['bajo_stock']}\n"
            mensaje += f"🚫 Sin stock: {stats['sin_stock']}\n\n"
            
            if productos_bajo_stock:
                mensaje += "Productos críticos:\n"
                for producto in productos_bajo_stock[:5]:  # Show max 5 products
                    stock_minimo = producto[4] if len(producto) > 4 else 10
                    estado = "🚫 SIN STOCK" if producto[2] == 0 else f"⚠️ {producto[2]} unidades"
                    mensaje += f"• {producto[1]}: {estado}\n"
                
                if len(productos_bajo_stock) > 5:
                    mensaje += f"... y {len(productos_bajo_stock) - 5} más\n"
            
            messagebox.showwarning("Alertas de Inventario", mensaje)
        else:
            messagebox.showinfo("Sistema de Inventario", 
                              f"✅ Sistema iniciado correctamente\n\n"
                              f"📦 {stats['total_productos']} productos en inventario\n"
                              f"💰 Valor total: ${stats['valor_total']:,.2f}\n"
                              f"🎯 Todas las existencias están en niveles óptimos")

    def generar_pdf(self):
        try:
            # Try to import reportlab
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            from reportlab.lib.units import inch
        except ImportError:
            messagebox.showerror("Error", 
                                "No se puede generar PDF. Falta la librería 'reportlab'.\n\n"
                                "Instálela con: pip install reportlab")
            return
        
        productos = self.model.obtener_productos()
        stats = self.model.obtener_estadisticas()
        
        if not productos:
            messagebox.showinfo("Información", "No hay productos para generar reporte")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"reporte_inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
        if filename:
            try:
                doc = SimpleDocTemplate(filename, pagesize=A4)
                styles = getSampleStyleSheet()
                story = []
                
                # Title
                title_style = styles['Title']
                title = Paragraph("REPORTE DE INVENTARIO", title_style)
                story.append(title)
                story.append(Spacer(1, 12))
                
                # Date and stats
                date_style = styles['Normal']
                date_text = f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
                story.append(Paragraph(date_text, date_style))
                story.append(Spacer(1, 12))
                
                # Statistics summary
                stats_data = [
                    ['Total Productos', str(stats['total_productos'])],
                    ['Valor Total', f"${stats['valor_total']:,.2f}"],
                    ['Stock Bajo', str(stats['bajo_stock'])],
                    ['Sin Stock', str(stats['sin_stock'])]
                ]
                
                stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(stats_table)
                story.append(Spacer(1, 20))
                
                # Products table
                products_title = Paragraph("DETALLE DE PRODUCTOS", styles['Heading2'])
                story.append(products_title)
                story.append(Spacer(1, 12))
                
                # Table headers
                headers = ['ID', 'Producto', 'Cantidad', 'Precio', 'Stock Mínimo', 'Valor Total']
                data = [headers]
                
                # Add products
                for producto in productos:
                    stock_minimo = producto[4] if len(producto) > 4 else 10
                    valor_total = producto[2] * producto[3]
                    
                    row = [
                        str(producto[0]),
                        producto[1],
                        str(producto[2]),
                        f"${producto[3]:.2f}",
                        str(stock_minimo),
                        f"${valor_total:.2f}"
                    ]
                    
                    # Color code for low stock
                    if producto[2] <= stock_minimo:
                        data.append(row)
                    else:
                        data.append(row)
                
                products_table = Table(data, colWidths=[0.5*inch, 2*inch, 1*inch, 1*inch, 1*inch, 1*inch])
                products_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 9)
                ]))
                
                # Color low stock items
                for i, producto in enumerate(productos):
                    stock_minimo = producto[4] if len(producto) > 4 else 10
                    if producto[2] <= stock_minimo:
                        products_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, i+1), (-1, i+1), colors.lightcoral)
                        ]))
                
                story.append(products_table)
                
                # Build PDF
                doc.build(story)
                
                messagebox.showinfo("Éxito", f"Reporte PDF generado: {filename}")
                
                # Try to open the PDF
                try:
                    if os.name == 'nt':  # Windows
                        os.startfile(filename)
                    elif os.name == 'posix':  # macOS and Linux
                        os.system(f'open "{filename}"' if os.uname().sysname == 'Darwin' else f'xdg-open "{filename}"')
                except:
                    pass
                    
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar el PDF: {str(e)}")

    def backup_database(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        default_filename = f"inventario_backup_{timestamp}.db"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if filename:
            try:
                self.model.backup_database(filename)
                messagebox.showinfo("Éxito", f"Copia de seguridad creada:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear la copia de seguridad:\n{str(e)}")

    def restore_database(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Database files", "*.db"), ("All files", "*.*")],
            title="Seleccionar copia de seguridad para restaurar"
        )
        
        if filename:
            # Confirm restore
            if not messagebox.askyesno(
                "Confirmar Restauración",
                "⚠️ ADVERTENCIA: Esta acción reemplazará toda la base de datos actual\n"
                "con los datos de la copia de seguridad seleccionada.\n\n"
                "¿Desea continuar?"
            ):
                return
            
            try:
                self.model.restore_database(filename)
                
                # Refresh UI
                self.cargar_productos()
                self.actualizar_estadisticas()
                
                messagebox.showinfo(
                    "Éxito", 
                    f"Base de datos restaurada exitosamente desde:\n{filename}\n\n"
                    "La interfaz se ha actualizado con los datos restaurados."
                )
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo restaurar la base de datos:\n{str(e)}")

    def exportar_csv(self):
        productos = self.model.obtener_productos()
        
        if not productos:
            messagebox.showinfo("Información", "No hay productos para exportar")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['ID', 'Producto', 'Cantidad', 'Precio', 'Stock Mínimo', 'Valor Total'])
                    
                    for producto in productos:
                        stock_minimo = producto[4] if len(producto) > 4 else 10
                        valor_total = producto[2] * producto[3]
                        writer.writerow([producto[0], producto[1], producto[2], producto[3], stock_minimo, valor_total])
                
                messagebox.showinfo("Éxito", f"Se exportaron {len(productos)} productos a {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")