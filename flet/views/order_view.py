import flet as ft
from controllers.order_controller import OrdenController
import datetime

class OrdenView:
    def __init__(self, page):
        self.page = page
        self.controller = OrdenController()
        self.contenedor_items = ft.Column()
        self.setup_ui()
    
    def setup_ui(self):
        # Referencias
        self.numero_orden = ft.Ref[ft.TextField]()
        self.fecha_emision = ft.Ref[ft.TextField]()
        self.proveedor_combo = ft.Ref[ft.Dropdown]()
        self.domicilio_fiscal = ft.Ref[ft.TextField]()
        self.telefono = ft.Ref[ft.TextField]()
        self.correo = ft.Ref[ft.TextField]()
        self.rubro = ft.Ref[ft.TextField]()
        self.observacion = ft.Ref[ft.TextField]()
        self.tasa_cambio = ft.Ref[ft.TextField]()
        
        # Campos de totales
        self.subtotal_field = ft.TextField(label="SUBTOTAL", value="$ 0.00", read_only=True, width=200)
        self.total_usd_field = ft.TextField(label="TOTAL $", value="$ 0.00", read_only=True, width=200)
        self.total_bsd_field = ft.TextField(label="TOTAL BSD", value="BS. 0.00", read_only=True, width=200)
        
        # Cargar proveedores
        self.cargar_proveedores()
    
    def cargar_proveedores(self):
        proveedores = self.controller.obtener_proveedores()
        options = [ft.dropdown.Option(f"{p['nombre']}") for p in proveedores]
        if self.proveedor_combo.current:
            self.proveedor_combo.current.options = options
    
    def cargar_datos_proveedor(self, e):
        proveedor_nombre = self.proveedor_combo.current.value
        if proveedor_nombre:
            proveedores = self.controller.obtener_proveedores()
            proveedor = next((p for p in proveedores if p['nombre'] == proveedor_nombre), None)
            if proveedor:
                self.domicilio_fiscal.current.value = proveedor.get('domicilio', '')
                self.telefono.current.value = proveedor.get('telefono', '')
                self.correo.current.value = proveedor.get('correo', '')
                self.rubro.current.value = proveedor.get('rubro', '')
                self.page.update()
    
    def agregar_item_ui(self, e):
        # Crear controles para nuevo item
        cantidad = ft.TextField(label="Cantidad", width=100)
        unidad = ft.TextField(label="Unidad", width=100, value="UND")
        descripcion = ft.TextField(label="Descripción", width=200)
        precio_unitario = ft.TextField(label="Precio Unitario", width=120)
        total = ft.TextField(label="Total", width=120, read_only=True)
        
        def calcular_total_item(e):
            try:
                cant = float(cantidad.value or 0)
                precio = float(precio_unitario.value or 0)
                total.value = f"$ {cant * precio:,.2f}"
            except:
                total.value = "$ 0.00"
            self.page.update()
        
        cantidad.on_change = calcular_total_item
        precio_unitario.on_change = calcular_total_item
        
        fila_item = ft.Row(controls=[
            cantidad, unidad, descripcion, precio_unitario, total,
            ft.TextButton("Eliminar", on_click=lambda e, row=fila_item: self.eliminar_item_ui(e, row))
        ])
        
        self.contenedor_items.controls.append(fila_item)
        self.page.update()
    
    def eliminar_item_ui(self, e, fila):
        self.contenedor_items.controls.remove(fila)
        self.page.update()
    
    def guardar_orden_ui(self, e):
        # Recoger datos de los items
        items = []
        for fila in self.contenedor_items.controls:
            controles = fila.controls
            items.append({
                'cantidad': controles[0].value,
                'unidad': controles[1].value,
                'descripcion': controles[2].value,
                'precio_unitario': controles[3].value,
                'total': controles[4].value.replace('$', '').replace(',', '').strip()
            })
        
        # Datos de la orden
        datos_orden = {
            'numero_orden': self.numero_orden.current.value,
            'fecha_emision': self.fecha_emision.current.value,
            'proveedor_id': 1,  # Aquí deberías obtener el ID real del proveedor
            'observacion': self.observacion.current.value,
            'tasa_cambio': self.tasa_cambio.current.value
        }
        
        # Guardar mediante el controlador
        orden_id = self.controller.guardar_orden(datos_orden)
        if orden_id:
            self.mostrar_dialogo("¡Éxito!", f"Orden guardada con ID: {orden_id}")
        else:
            self.mostrar_dialogo("Error", "No se pudo guardar la orden")
    
    def mostrar_dialogo(self, titulo, mensaje):
        dialog = ft.AlertDialog(
            title=ft.Text(titulo),
            content=ft.Text(mensaje),
            actions=[ft.TextButton("OK", on_click=lambda e: self.cerrar_dialogo(e))]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def cerrar_dialogo(self, e):
        self.page.dialog.open = False
        self.page.update()
    
    def get_view(self):
        return ft.Column([
            # Encabezado
            ft.Row([ft.Text("Mi Super", size=24, weight=ft.FontWeight.BOLD)], 
                   alignment=ft.MainAxisAlignment.CENTER),
            
            # Información del proveedor
            ft.Card(content=ft.Container(padding=20, content=ft.Column([
                ft.Row([
                    ft.Text("Señores:", width=100),
                    ft.Dropdown(ref=self.proveedor_combo, label="Proveedor", width=300,
                               on_change=self.cargar_datos_proveedor),
                    ft.Text("Nº orden:", width=100),
                    ft.TextField(ref=self.numero_orden, label="Número", width=150),
                ]),
                ft.Row([
                    ft.Text("Fecha:", width=100),
                    ft.TextField(ref=self.fecha_emision, label="Fecha", width=150,
                                value=datetime.datetime.now().strftime("%d/%m/%Y")),
                ]),
            ]))),
            
            # Información de contacto
            ft.Card(content=ft.Container(padding=20, content=ft.Column([
                ft.TextField(ref=self.domicilio_fiscal, label="Dom. Fiscal", expand=True, read_only=True),
                ft.Row([
                    ft.TextField(ref=self.telefono, label="Teléfono", width=200, read_only=True),
                    ft.TextField(ref=self.correo, label="Correo", expand=True, read_only=True),
                ]),
                ft.TextField(ref=self.rubro, label="Rubro", expand=True, read_only=True),
            ]))),
            
            # Items de compra
            ft.Card(content=ft.Container(padding=20, content=ft.Column([
                ft.Text("Items de Compra:", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Text("Cantidad", width=100), ft.Text("Unidad", width=100),
                    ft.Text("Descripción", width=200), ft.Text("Precio", width=120),
                    ft.Text("Total", width=120), ft.Container(width=60)
                ]),
                self.contenedor_items,
                ft.ElevatedButton("Agregar Item", on_click=self.agregar_item_ui)
            ]))),
            
            # Totales
            ft.Card(content=ft.Container(padding=20, content=ft.Column([
                ft.Row([self.subtotal_field]),
                ft.Text("OBSERVACIÓN:", weight=ft.FontWeight.BOLD),
                ft.TextField(ref=self.observacion, label="Observación", multiline=True),
                ft.Row([self.total_usd_field]),
                ft.Row([
                    ft.Text("TASA BS.:", width=100),
                    ft.TextField(ref=self.tasa_cambio, label="Tasa", width=150),
                ]),
                ft.Row([self.total_bsd_field]),
            ]))),
            
            # Botones
            ft.Row([
                ft.ElevatedButton("Guardar", on_click=self.guardar_orden_ui,
                                 style=ft.ButtonStyle(color="white", bgcolor="green")),
                ft.TextButton("Limpiar", on_click=lambda e: self.controller.limpiar_orden()),
            ])
        ])