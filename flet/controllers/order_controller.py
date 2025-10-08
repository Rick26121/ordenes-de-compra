from models.database import Database
from models.proveedor import Proveedor
from models.orden_compra import OrdenCompra

class OrdenController:
    def __init__(self):
        self.db = Database()
        self.orden_actual = OrdenCompra()
    
    def obtener_proveedores(self):
        return Proveedor.get_all_proveedores(self.db)
    
    def obtener_proveedor(self, proveedor_id):
        return Proveedor.get_proveedor_by_id(self.db, proveedor_id)
    
    def agregar_item(self, cantidad, unidad, descripcion, precio_unitario):
        total = float(cantidad) * float(precio_unitario)
        item = {
            'cantidad': cantidad,
            'unidad': unidad,
            'descripcion': descripcion,
            'precio_unitario': precio_unitario,
            'total': total
        }
        self.orden_actual.items.append(item)
        self.calcular_totales()
        return item
    
    def eliminar_item(self, index):
        if 0 <= index < len(self.orden_actual.items):
            self.orden_actual.items.pop(index)
            self.calcular_totales()
    
    def calcular_totales(self):
        subtotal = sum(float(item['total']) for item in self.orden_actual.items)
        self.orden_actual.subtotal = subtotal
        self.orden_actual.total_usd = subtotal
        
        if self.orden_actual.tasa_cambio > 0:
            self.orden_actual.total_bsd = subtotal * float(self.orden_actual.tasa_cambio)
        else:
            self.orden_actual.total_bsd = 0
    
    def guardar_orden(self, datos_orden):
        # Actualizar datos de la orden
        self.orden_actual.numero_orden = datos_orden['numero_orden']
        self.orden_actual.fecha_emision = datos_orden['fecha_emision']
        self.orden_actual.proveedor_id = datos_orden['proveedor_id']
        self.orden_actual.observacion = datos_orden['observacion']
        self.orden_actual.tasa_cambio = datos_orden['tasa_cambio']
        
        # Calcular totales finales
        self.calcular_totales()
        
        # Guardar en base de datos
        orden_id = self.orden_actual.guardar_orden(self.db)
        return orden_id
    
    def limpiar_orden(self):
        self.orden_actual = OrdenCompra()