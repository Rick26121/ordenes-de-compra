import flet as ft
import datetime

def main(page: ft.Page):
    page.title = "Órdenes de Compra/Pago"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.ADAPTIVE

    # Lista de proveedores predefinidos (puedes agregar más)
    proveedores = [
    "INVERSIONES NAZAR",
    "DISTRIBUIDORA COMERCIAL XYZ",
    "FERRETERÍA EL MARTILLO",
    "ELECTRODOMÉSTICOS SA",
    "PAPELERÍA OFICENTER"
    ]

    # Variables para los datos
    numero_orden = ft.Ref[ft.TextField]()
    fecha_emision = ft.Ref[ft.TextField]()
    proveedor_combo = ft.Ref[ft.Dropdown]()
    domicilio_fiscal = ft.Ref[ft.TextField]()
    telefono = ft.Ref[ft.TextField]()
    correo = ft.Ref[ft.TextField]()
    rubro = ft.Ref[ft.TextField]()
    observacion = ft.Ref[ft.TextField]()
    tasa_cambio = ft.Ref[ft.TextField]()
    
    # Lista para items de compra
    items_compra = []
    
    # Función para cargar datos del proveedor seleccionado
    def cargar_datos_proveedor(e):
        proveedor_seleccionado = proveedor_combo.current.value
        if proveedor_seleccionado == "INVERSIONES NAZAR":
            domicilio_fiscal.current.value = "Fachura/ Nota de Entrega/Cotización:"
            telefono.current.value = "0414-1234567"
            correo.current.value = "inversionesnazar@email.com"
            rubro.current.value = "Ferretería y Materiales"
        elif proveedor_seleccionado == "DISTRIBUIDORA COMERCIAL XYZ":
            domicilio_fiscal.current.value = "Av. Principal, Centro"
            telefono.current.value = "0424-9876543"
            correo.current.value = "xyzcomercial@email.com"
            rubro.current.value = "Distribución General"
        elif proveedor_seleccionado == "FERRETERÍA EL MARTILLO":
            domicilio_fiscal.current.value = "Zona Industrial"
            telefono.current.value = "0412-5556666"
            correo.current.value = "martilloferre@email.com"
            rubro.current.value = "Ferretería"
        elif proveedor_seleccionado == "ELECTRODOMÉSTICOS SA":
            domicilio_fiscal.current.value = "Centro Comercial Mega"
            telefono.current.value = "0416-7778888"
            correo.current.value = "electrosa@email.com"
            rubro.current.value = "Electrodomésticos"
        elif proveedor_seleccionado == "PAPELERÍA OFICENTER":
            domicilio_fiscal.current.value = "Av. Bolívar Este"
            telefono.current.value = "0426-3332222"
            correo.current.value = "oficenter@email.com"
            rubro.current.value = "Papelería y Oficina"
        else:
            # Limpiar campos si no hay selección
            domicilio_fiscal.current.value = ""
            telefono.current.value = ""
            correo.current.value = ""
            rubro.current.value = ""
        
        page.update()
    
    def agregar_item(e):
        # Crear nuevo item
        nuevo_item = {
            "cantidad": ft.TextField(label="Cantidad", width=100),
            "unidad": ft.TextField(label="Unidad", width=100, value="UND"),
            "descripcion": ft.TextField(label="Descripción", width=200),
            "precio_unitario": ft.TextField(label="Precio Unitario", width=120),
            "total": ft.TextField(label="Total", width=120, read_only=True)
        }
        
        # Función para calcular total
        def calcular_total(e):
            try:
                cantidad = float(nuevo_item["cantidad"].value or 0)
                precio = float(nuevo_item["precio_unitario"].value or 0)
                total = cantidad * precio
                nuevo_item["total"].value = f"$ {total:,.2f}"
            except:
                nuevo_item["total"].value = "$ 0.00"
            calcular_totales()
        
        # Asignar eventos
        nuevo_item["cantidad"].on_change = calcular_total
        nuevo_item["precio_unitario"].on_change = calcular_total
        
        # Crear fila
        fila_item = ft.Row(
            controls=[
                nuevo_item["cantidad"],
                nuevo_item["unidad"],
                nuevo_item["descripcion"],
                nuevo_item["precio_unitario"],
                nuevo_item["total"],
                ft.TextButton(
                    "Eliminar",
                    on_click=lambda e, item=nuevo_item: eliminar_item(e, item)
                )
            ]
        )
        
        items_compra.append({"fila": fila_item, "campos": nuevo_item})
        contenedor_items.controls.append(fila_item)
        page.update()

    def eliminar_item(e, item):
        contenedor_items.controls.remove(item["fila"])
        items_compra.remove(item)
        calcular_totales()
        page.update()

    def calcular_totales(e=None):
        try:
            subtotal = 0
            for item in items_compra:
                try:
                    cantidad = float(item["campos"]["cantidad"].value or 0)
                    precio = float(item["campos"]["precio_unitario"].value or 0)
                    subtotal += cantidad * precio
                except:
                    continue
            
            # Calcular total en dólares
            total_usd = subtotal
            
            # Calcular total en bolívares
            try:
                tasa = float(tasa_cambio.current.value or 0)
                total_bsd = total_usd * tasa
            except:
                total_bsd = 0
            
            # Actualizar campos
            subtotal_field.value = f"$ {subtotal:,.2f}"
            total_usd_field.value = f"$ {total_usd:,.2f}"
            total_bsd_field.value = f"BS. {total_bsd:,.2f}"
            
        except Exception as ex:
            print(f"Error en cálculo: {ex}")
        
        page.update()

    def limpiar_formulario(e):
        # Limpiar campos principales
        proveedor_combo.current.value = None
        for ref in [numero_orden, fecha_emision, domicilio_fiscal, 
                   telefono, correo, rubro, observacion, tasa_cambio]:
            ref.current.value = ""
        
        # Restaurar fecha actual
        fecha_emision.current.value = datetime.datetime.now().strftime("%d/%m/%Y")
        
        # Limpiar items
        contenedor_items.controls.clear()
        items_compra.clear()
        
        # Limpiar totales
        subtotal_field.value = "$ 0.00"
        total_usd_field.value = "$ 0.00"
        total_bsd_field.value = "BS. 0.00"
        
        page.update()

    def guardar_orden(e):
        # Validar campos obligatorios
        if not proveedor_combo.current.value:
            mostrar_error("Seleccione un proveedor")
            return
            
        if not numero_orden.current.value:
            mostrar_error("Ingrese el número de orden")
            return
        
        # Aquí iría la lógica para guardar en BD
        datos = {
            "numero_orden": numero_orden.current.value,
            "fecha_emision": fecha_emision.current.value,
            "proveedor": proveedor_combo.current.value,
            "domicilio": domicilio_fiscal.current.value,
            "telefono": telefono.current.value,
            "correo": correo.current.value,
            "rubro": rubro.current.value,
            "items": [
                {
                    "cantidad": item["campos"]["cantidad"].value,
                    "unidad": item["campos"]["unidad"].value,
                    "descripcion": item["campos"]["descripcion"].value,
                    "precio_unitario": item["campos"]["precio_unitario"].value,
                    "total": item["campos"]["total"].value
                }
                for item in items_compra
            ],
            "subtotal": subtotal_field.value,
            "total_usd": total_usd_field.value,
            "total_bsd": total_bsd_field.value,
            "observacion": observacion.current.value,
            "tasa_cambio": tasa_cambio.current.value
        }
        
        print("Datos a guardar:", datos)
        page.dialog = dlg_guardado
        dlg_guardado.open = True
        page.update()

    def mostrar_error(mensaje):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(mensaje),
            actions=[ft.TextButton("OK", on_click=lambda e: cerrar_dialogo(e))]
        )
        page.dialog.open = True
        page.update()

    def cerrar_dialogo(e):
        page.dialog.open = False
        page.update()

    # Campos de totales
    subtotal_field = ft.TextField(label="SUBTOTAL", value="$ 0.00", read_only=True, width=200)
    total_usd_field = ft.TextField(label="TOTAL $", value="$ 0.00", read_only=True, width=200)
    total_bsd_field = ft.TextField(label="TOTAL BSD", value="BS. 0.00", read_only=True, width=200)

    # Diálogo de confirmación
    dlg_guardado = ft.AlertDialog(
        title=ft.Text("¡Orden Guardada!"),
        content=ft.Text("La orden de compra/pago se ha guardado exitosamente."),
        actions=[ft.TextButton("OK", on_click=cerrar_dialogo)]
    )

    # Contenedor para items dinámicos
    contenedor_items = ft.Column()

    # Interfaz principal
    page.add(
        ft.Column([
            # Encabezado
            ft.Row([
                ft.Text("Mi Super", size=24, weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Row([
                ft.Text("ORDEN DE COMPRA ______", size=16),
                ft.Text("ORDEN DE PAGO ______", size=16),
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            
            # Información del proveedor
            ft.Card(
                content=ft.Container(
                    padding=20,
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Señores:", width=100),
                            ft.Dropdown(
                                ref=proveedor_combo,
                                label="Seleccione Proveedor",
                                options=[ft.dropdown.Option(prov) for prov in proveedores],
                                width=300,
                                on_change=cargar_datos_proveedor
                            ),
                            ft.Text("Nº de orden:", width=100),
                            ft.TextField(ref=numero_orden, label="Número", width=150),
                        ]),
                        ft.Row([
                            ft.Text("Fecha de Emisión:", width=120),
                            ft.TextField(ref=fecha_emision, label="Fecha", width=150, 
                                       value=datetime.datetime.now().strftime("%d/%m/%Y")),
                        ]),
                    ])
                )
            ),
            
            # Información de contacto (se llena automáticamente)
            ft.Card(
                content=ft.Container(
                    padding=20,
                    content=ft.Column([
                        ft.Row([
                            ft.TextField(ref=domicilio_fiscal, label="Dom. Fiscal", expand=True, read_only=True),
                        ]),
                        ft.Row([
                            ft.TextField(ref=telefono, label="Teléfonos", width=200, read_only=True),
                            ft.TextField(ref=correo, label="Correo", expand=True, read_only=True),
                        ]),
                        ft.Row([
                            ft.TextField(ref=rubro, label="Rubro", expand=True, read_only=True),
                        ]),
                    ])
                )
            ),
            
            # Tabla de items
            ft.Card(
                content=ft.Container(
                    padding=20,
                    content=ft.Column([
                        ft.Text("Items de Compra:", size=16, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            ft.Text("Cantidad", width=100),
                            ft.Text("Unidad", width=100),
                            ft.Text("Descripción", width=200),
                            ft.Text("Precio unitario", width=120),
                            ft.Text("Total", width=120),
                            ft.Container(width=60)
                        ]),
                        contenedor_items,
                        ft.ElevatedButton(
                            "Agregar Item",
                            on_click=agregar_item
                        )
                    ])
                )
            ),
            
            # Totales
            ft.Card(
                content=ft.Container(
                    padding=20,
                    content=ft.Column([
                        ft.Row([subtotal_field]),
                        ft.Text("OBSERVACIÓN:", weight=ft.FontWeight.BOLD),
                        ft.TextField(ref=observacion, label="Observación", multiline=True, min_lines=2),
                        ft.Row([total_usd_field]),
                        ft.Row([
                            ft.Text("TASA BOY BS.:", width=120),
                            ft.TextField(ref=tasa_cambio, label="Tasa de Cambio", width=150, on_change=calcular_totales),
                        ]),
                        ft.Row([total_bsd_field]),
                    ])
                )
            ),
            
            # Botones de acción
            ft.Row([
                ft.ElevatedButton(
                    "Guardar Orden",
                    on_click=guardar_orden,
                    style=ft.ButtonStyle(color="white", bgcolor="green")
                ),
                ft.TextButton(
                    "Limpiar Formulario",
                    on_click=limpiar_formulario
                ),
            ])
        ])
    )

ft.app(target=main)