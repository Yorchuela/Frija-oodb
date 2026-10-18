
from repository import RepositorioCerveceria


def main():
    repositorio = RepositorioCerveceria()

    try:
        print("=== PRUEBA CRUD Y TRANSACCIONES ===")

        # 1. CREATE: crear un producto
        producto = repositorio.crear_producto(
            nombre="Cerveza de prueba CRUD",
            marca="Frija",
            categoria="Experimental",
            presentacion="Botella",
            contenido_ml=355,
            alcohol=5.0,
            precio=40.00,
        )
        repositorio.guardar()
        print(f"CREATE: producto {producto.producto_id} creado.")

        # 2. READ: consultar el producto
        encontrado = repositorio.obtener_producto(
            producto.producto_id
        )
        print(
            "READ:",
            encontrado.descripcion()
            if encontrado else "Producto no encontrado"
        )

        # 3. UPDATE: modificar el precio
        actualizado = repositorio.actualizar_precio(
            producto.producto_id, 45.00
        )
        repositorio.guardar()

        producto_actualizado = repositorio.obtener_producto(
            producto.producto_id
        )
        print(
            "UPDATE:",
            f"precio actualizado a ${producto_actualizado.precio:.2f}"
            if actualizado else "No se pudo actualizar"
        )

        # 4. Crear inventario relacionado con el producto
        inventario = repositorio.crear_inventario(
            sucursal="Tijuana",
            producto_id=producto.producto_id,
            stock=20,
            stock_minimo=5,
        )
        repositorio.guardar()

        print(
            "RELACIÓN:",
            f"Inventario {inventario.inventario_id} referencia "
            f"al producto {inventario.producto.producto_id}."
        )

        # 5. Consultar inventario bajo
        inventarios_bajos = repositorio.inventario_bajo()
        print(
            "CONSULTA:",
            f"Se encontraron {len(inventarios_bajos)} inventarios bajos."
        )

        # 6. DELETE: eliminar primero el inventario
        eliminado_inventario = repositorio.eliminar_inventario(
            inventario.inventario_id
        )
        repositorio.guardar()
        print(
            "DELETE INVENTARIO:",
            "correcto" if eliminado_inventario else "no encontrado"
        )

        # Ahora se puede eliminar el producto
        eliminado_producto = repositorio.eliminar_producto(
            producto.producto_id
        )
        repositorio.guardar()
        print(
            "DELETE PRODUCTO:",
            "correcto" if eliminado_producto else "no encontrado"
        )

        # 7. COMMIT: crear un producto que debe conservarse
        confirmado = repositorio.crear_producto(
            nombre="Producto confirmado",
            marca="Frija",
            categoria="Prueba",
            presentacion="Lata",
            contenido_ml=473,
            alcohol=4.5,
            precio=35.00,
        )
        repositorio.guardar()

        print(
            "COMMIT:",
            "producto guardado"
            if repositorio.obtener_producto(confirmado.producto_id)
            else "ERROR"
        )

        # 8. ABORT: crear un producto y revertir el cambio
        temporal = repositorio.crear_producto(
            nombre="Producto temporal abort",
            marca="Prueba",
            categoria="Prueba",
            presentacion="Lata",
            contenido_ml=473,
            alcohol=4.0,
            precio=30.00,
        )
        id_temporal = temporal.producto_id

      
        repositorio.deshacer_cambios()

        print(
            "ABORT:",
            "cambio revertido"
            if repositorio.obtener_producto(id_temporal) is None
            else "REVISAR: el producto sigue presente"
        )

        # 9. Prueba de herencia y polimorfismo
        print("\n=== HERENCIA Y POLIMORFISMO ===")

        nacional = repositorio.crear_producto(
            nombre="Cerveza Nacional Demo",
            marca="Frija",
            categoria="Lager",
            presentacion="Botella",
            contenido_ml=355,
            alcohol=5.0,
            precio=40.00,
            importado=False,
        )

        importada = repositorio.crear_producto(
            nombre="Cerveza Importada Demo",
            marca="Frija",
            categoria="Ale",
            presentacion="Lata",
            contenido_ml=473,
            alcohol=6.0,
            precio=55.00,
            importado=True,
        )

        repositorio.guardar()

        # El mismo método se comporta diferente según la clase
        for producto in (nacional, importada):
            print(producto.descripcion())

            
        # 10. Prueba de consultas y relaciones
        print("\n=== CONSULTAS DE OBJETOS ===")

        producto_consulta = repositorio.crear_producto(
            nombre="Cerveza Consulta Demo",
            marca="Frija",
            categoria="ConsultaTest",
            presentacion="Lata",
            contenido_ml=473,
            alcohol=5.0,
            precio=38.00,
        )

        inventario_consulta = repositorio.crear_inventario(
            sucursal="Tijuana",
            producto_id=producto_consulta.producto_id,
            stock=2,
            stock_minimo=5,
        )

        envio_consulta = repositorio.crear_envio(
            cliente="Cliente Demo",
            sucursal="Tijuana",
            direccion="Tijuana, Baja California",
        )

        repositorio.agregar_producto_envio(
            envio_consulta.envio_id,
            producto_consulta.producto_id,
            3,
        )

        repositorio.guardar()

        # Consulta 1: productos por categoría
        productos = repositorio.productos_por_categoria(
            "ConsultaTest"
        )
        print("Productos por categoría:", len(productos))

        # Consulta 2: inventario por debajo del mínimo
        bajos = repositorio.inventario_bajo()
        print("Inventarios bajos:", len(bajos))

        # Consulta 3: envíos pendientes
        pendientes = repositorio.envios_pendientes()
        print("Envíos pendientes:", len(pendientes))

        # Comprobar la relación del envío con el producto
        print("Descripción del envío:", envio_consulta.descripcion())
        print(
            "Producto del detalle:",
            envio_consulta.detalles[0]["producto"].descripcion(),

            
        )

        
        # 11. Prueba de eliminación en cascada
        print("\n=== ELIMINACIÓN EN CASCADA ===")

        id_envio_prueba = envio_consulta.envio_id

        resultado = repositorio.eliminar_envio(id_envio_prueba)

        print("ELIMINACIÓN EN CASCADA:", resultado)
        print("DETALLES RESTANTES:", len(envio_consulta.detalles))

        repositorio.guardar()



    finally:
        repositorio.cerrar()


if __name__ == "__main__":
    main()


