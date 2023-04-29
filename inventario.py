import mysql.connector
import sys

conexion = None

try:

    def getconexion():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="inventario"
        )

    def createTables():
        tables = ["CREATE TABLE IF NOT EXISTS inventario (id INT AUTO_INCREMENT PRIMARY KEY, nombreProducto VARCHAR(255) NOT NULL, cantidad INT NOT NULL, precio DECIMAL(10,2) NOT NULL)"]
        conexion = getconexion()
        cursor = conexion.cursor()
        for table in tables:
            cursor.execute(table)


    def principal():
        createTables()
        menu = """
    \n------------------------------------------
            SISTEMA DE INVENTARIO
    a) Agregar nuevo producto:
    b) Editar producto existente:
    c) Eliminar producto existente:
    d) Ver lista de productos:
    e) Buscar producto por nombre:
    f) Salir
    ---------------------------------------------
    Selecciona una opción: """

        option = ""
        while option != "f":
            option = input(menu)
            if option == "a":
                nombre = input("Ingresa el nombre del producto: ")
                product = obtenerProducto(nombre)
                if product is not None:
                    print(f"El producto '{nombre}' ya existe")
                else:
                    cantidad = int(input("Ingresa la cantidad: "))
                    precio = float(input("Ingresa el precio: "))
                    agregarProducto(nombre, cantidad, precio)
                    print(f"Producto agregado: {nombre}")
            if option == "b":
                nombre = input("Ingresa el nombre del producto que quieres editar: ")
                cantidad = int(input("Ingresa la nueva cantidad: "))
                precio = float(input("Ingresa el nuevo precio: "))
                editarProducto(nombre, cantidad, precio)
                print(f"Producto actualizado: {nombre}")
            if option == "c":
                nombre = input("Ingresa el nombre del producto a eliminar: ")
                eliminarProducto(nombre)
                print(f"Producto eliminado: {nombre}")
            if option == "d":
                products = obtenerProductos()
                print("=== Lista de productos ===")
                print("Nombre Producto         -    Precio             -      Stock       ")
                for product in products:
                    print(f"{product[0]}       -    {product[2]}       -      {product[1]}")
            if option == "e":
                nombre = input("Ingresa el nombre del producto que deseas buscar: ")
                product = obtenerProducto(nombre)
                if product is not None:
                    print(f"El producto '{nombre}' tiene una cantidad de {product[0]} y un precio de {product[1]}")
                else:
                    print(f"Producto '{nombre}' no encontrado")
        else:
            print("\nEl programa ha finalizado,bye...")
            sys.exit()

    def agregarProducto(nombre, cantidad, precio):
        conexion = getconexion()
        cursor = conexion.cursor()
        declarar = "INSERT INTO inventario (nombreProducto, cantidad, precio) VALUES (%s, %s, %s)"
        cursor.execute(declarar, (nombre, cantidad, precio))
        conexion.commit()

    def editarProducto(nombre, cantidad, precio):
        conexion = getconexion()
        cursor = conexion.cursor()
        declarar = "UPDATE inventario SET cantidad = %s, precio = %s WHERE nombreProducto = %s"
        cursor.execute(declarar, (cantidad, precio, nombre))
        conexion.commit()

    def eliminarProducto(nombre):
        conexion = getconexion()
        cursor = conexion.cursor()
        declarar = "DELETE FROM inventario WHERE nombreProducto = %s"
        cursor.execute(declarar, (nombre,))
        conexion.commit()

    def obtenerProductos():
        conexion = getconexion()
        cursor = conexion.cursor()
        query = "SELECT nombreProducto, cantidad, precio FROM inventario"
        cursor.execute(query)
        return cursor.fetchall()

    def obtenerProducto(nombre):
        conexion = getconexion()
        cursor = conexion.cursor()
        query = "SELECT cantidad, precio FROM inventario WHERE nombreProducto = %s"
        cursor.execute(query, (nombre,))
        return cursor.fetchone()

    if __name__ == '__main__':
        principal()


finally:
    
    if conexion is not None:
        getconexion().close