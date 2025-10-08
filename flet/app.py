import flet as ft
from views.order_view import OrdenView

def main(page: ft.Page):
    page.title = "Sistema Órdenes de Compra"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.ADAPTIVE
    
    # Crear vista
    orden_view = OrdenView(page)
    
    # Agregar vista a la página
    page.add(orden_view.get_view())

ft.app(target=main)