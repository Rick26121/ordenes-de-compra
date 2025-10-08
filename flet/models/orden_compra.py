from datetime import datetime

class OrdenCompra:
    def __init__(self):
        self.id = None
        self.numero_orden = ""
        self.fecha_emision = datetime.now().strftime("%d/%m/%Y")
        self.proveedor_id = None
        self.observacion = ""
        self.tasa_cambio = 0.0
        self.subtotal = 0.0
        self.total_usd = 0.0
        self.total_bsd = 0.0
        self.items = []
    
    def guardar_orden(self, db):
        connection = db.connect()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Insertar orden principal
                cursor.execute("""
                    INSERT INTO ordenes_compra 
                    (numero_orden, fecha_emision, proveedor_id, observacion, tasa_cambio, subtotal, total_usd, total_bsd)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (self.numero_orden, self.fecha_emision, self.proveedor_id, self.observacion, 
                      self.tasa_cambio, self.subtotal, self.total_usd, self.total_bsd))
                
                orden_id = cursor.lastrowid
                
                # Insertar items
                for item in self.items:
                    cursor.execute("""
                        INSERT INTO orden_items 
                        (orden_id, cantidad, unidad, descripcion, precio_unitario, total)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (orden_id, item['cantidad'], item['unidad'], item['descripcion'], 
                          item['precio_unitario'], item['total']))
                
                connection.commit()
                return orden_id
                
            except Error as e:
                connection.rollback()
                print(f"Error guardando orden: {e}")
                return None
            finally:
                cursor.close()
                db.disconnect()
        return None