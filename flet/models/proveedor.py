class Proveedor:
    def __init__(self, id=None, nombre=None, rif=None, domicilio=None, telefono=None, correo=None, rubro=None):
        self.id = id
        self.nombre = nombre
        self.rif = rif
        self.domicilio = domicilio
        self.telefono = telefono
        self.correo = correo
        self.rubro = rubro
    
    @staticmethod
    def get_all_proveedores(db):
        connection = db.connect()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM proveedores")
                proveedores = cursor.fetchall()
                return proveedores
            except Error as e:
                print(f"Error obteniendo proveedores: {e}")
                return []
            finally:
                cursor.close()
                db.disconnect()
        return []
    
    @staticmethod
    def get_proveedor_by_id(db, proveedor_id):
        connection = db.connect()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM proveedores WHERE id = %s", (proveedor_id,))
                proveedor = cursor.fetchone()
                return proveedor
            except Error as e:
                print(f"Error obteniendo proveedor: {e}")
                return None
            finally:
                cursor.close()
                db.disconnect()
        return None