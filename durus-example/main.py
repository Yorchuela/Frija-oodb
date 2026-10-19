
import os
import tempfile

from repository import RepositorioCerveceria


def probar_validaciones(repositorio):
    """Comprueba que el sistema rechace datos inválidos."""

    print("\n=== PRUEBAS DE VALIDACIÓN ===")

    pruebas_correctas = 0
    total_pruebas = 6

    # 1. Rechazar un precio negativo.
    try:
        repositorio.crear_producto(
            nombre="Producto inválido",
            marca="Frija",
            categoria="Pruebas",
            presentacion="Botella",
            contenido_ml=355,
            alcohol=5.0,
            precio=-10,
        )
        print("ERROR: se aceptó un precio negativo.")
    except ValueError:
        pruebas_correctas += 1
        print("OK: se rechazó el precio negativo.")

    # 2. Rechazar un porcentaje de alcohol superior a 100.
    try:
        repositorio.crear_producto(
            nombre="Producto inválido",
            marca="Frija",
            categoria="Pruebas",
            presentacion="Botella",
            contenido_ml=355,
            alcohol=120,
            precio=30,
        )
        print("ERROR: se aceptó un porcentaje de alcohol inválido.")
    except ValueError:
        pruebas_correctas += 1
        print("OK: se rechazó el porcentaje de alcohol inválido.")

    # 3. Rechazar un contenido infinito.
    try:
        repositorio.crear_producto(
            nombre="Producto inválido",
            marca="Frija",
            categoria="Pruebas",
            presentacion="Botella",
            contenido_ml=float("inf"),
            alcohol=5.0,
            precio=30,
        )
        print("ERROR: se aceptó un contenido infinito.")
    except ValueError:
        pruebas_correctas += 1
        print("OK: se rechazó el contenido infinito.")

    # 4. Rechazar un stock negativo.
    try:
        repositorio.crear_inventario(
            sucursal="Tijuana",
            producto_id=-999,
            stock=-5,
            stock_minimo=2,
        )
        print("ERROR: se aceptó un stock negativo.")
    except ValueError:
        pruebas_correctas += 1
        print("OK: se rechazó el stock negativo.")

    # 5. Rechazar un producto inexistente.
    try:
        repositorio.crear_inventario(
            sucursal="Tijuana",
            producto_id=-999,
            stock=5,
            stock_minimo=2,
        )
        print("ERROR: se aceptó un producto inexistente.")
    except ValueError:
        pruebas_correctas += 1
        print("OK: se rechazó el producto inexistente.")

    # 6. Rechazar una categoría vacía.
    try:
        repositorio.productos_por_categoria("   ")
        print("ERROR: se aceptó una categoría vacía.")
    except ValueError:
        pruebas_correctas += 1
        print("OK: se rechazó la categoría vacía.")

    print(
        f"\nResultado: {pruebas_correctas}/{total_pruebas} "
        "pruebas de validación correctas."
    )

    if pruebas_correctas != total_pruebas:
        raise AssertionError(
            "Una o más pruebas de validación fallaron."
        )


def main():
    os.makedirs("data", exist_ok=True)

    # Crear un archivo temporal exclusivo para las pruebas.
    archivo_temporal = tempfile.NamedTemporaryFile(
        prefix="cerveceria_pruebas_",
        suffix=".durus",
        dir="data",
        delete=False,
    )

    ruta_temporal = archivo_temporal.name
    archivo_temporal.close()
    os.remove(ruta_temporal)

    repositorio = None

    try:
        repositorio = RepositorioCerveceria(ruta=ruta_temporal)

        # 1. CRUD Y TRANSACCIONES.
        print("=== PRUEBA CRUD Y TRANSACCIONES ===")

        producto = repositorio.crear_producto(
            nombre="Cerveza de prueba CRUD",
            marca="Frija",
            categoria="CRUDTest",
            presentacion="Botella",
            contenido_ml=355,
            alcohol=5.0,
            precio=40.00,
        )

        repositorio.guardar()
        print(f"CREATE: producto {producto.producto_id} creado.")

        # READ.
        producto_leido = repositorio.obtener_producto(
            producto.producto_id
        )

        if producto_leido is not None:
            print("READ:", producto_leido.descripcion())
        else:
            raise AssertionError("No se encontró el producto creado.")

        # UPDATE.
        precio_anterior = producto_leido.precio

        resultado_precio = repositorio.actualizar_precio(
            producto.producto_id,
            45.00,
        )

        producto_actualizado = repositorio.obtener_producto(
            producto.producto_id
        )

        if not resultado_precio:
            raise AssertionError("No se pudo actualizar el precio.")

        print(
            "UPDATE: precio actualizado de "
            f"${precio_anterior:.2f} a "
            f"${producto_actualizado.precio:.2f}"
        )

        repositorio.guardar()

        # Crear inventario y comprobar la relación.
        inventario = repositorio.crear_inventario(
            sucursal="Tijuana",
            producto_id=producto.producto_id,
            stock=10,
            stock_minimo=5,
        )

        repositorio.guardar()

        print(
            "RELACIÓN: el inventario "
            f"{inventario.inventario_id} referencia al producto "
            f"{inventario.producto.producto_id}."
        )

        # DELETE: eliminar inventario y producto.
        resultado_inventario = repositorio.eliminar_inventario(
            inventario.inventario_id
        )

        repositorio.guardar()

        print(
            "DELETE INVENTARIO:",
            "correcto" if resultado_inventario else "no encontrado",
        )

        resultado_producto = repositorio.eliminar_producto(
            producto.producto_id
        )

        repositorio.guardar()

        print(
            "DELETE PRODUCTO:",
            "correcto" if resultado_producto else "no encontrado",
        )

        # COMMIT.
        producto_commit = repositorio.crear_producto(
            nombre="Cerveza Commit",
            marca="Frija",
            categoria="TransaccionesTest",
            presentacion="Lata",
            contenido_ml=355,
            alcohol=4.5,
            precio=35.00,
        )

        id_commit = producto_commit.producto_id
        repositorio.guardar()

        print(f"COMMIT: producto {id_commit} guardado.")

        # ABORT.
        producto_temporal = repositorio.crear_producto(
            nombre="Cerveza Temporal",
            marca="Frija",
            categoria="TransaccionesTest",
            presentacion="Botella",
            contenido_ml=355,
            alcohol=5.0,
            precio=30.00,
        )

        id_temporal = producto_temporal.producto_id

        repositorio.deshacer_cambios()

        producto_revertido = repositorio.obtener_producto(
            id_temporal
        )

        if producto_revertido is None:
            print("ABORT: correcto, el producto temporal no se guardó.")
        else:
            raise AssertionError(
                "ABORT falló: el producto temporal sigue existiendo."
            )

        # 2. HERENCIA Y POLIMORFISMO.
        print("\n=== HERENCIA Y POLIMORFISMO ===")

        cerveza_nacional = repositorio.crear_producto(
            nombre="Cerveza Nacional Demo",
            marca="Frija",
            categoria="HerenciaTest",
            presentacion="Botella",
            contenido_ml=355,
            alcohol=5.0,
            precio=40.00,
            importado=False,
        )

        cerveza_importada = repositorio.crear_producto(
            nombre="Cerveza Importada Demo",
            marca="Frija",
            categoria="HerenciaTest",
            presentacion="Lata",
            contenido_ml=355,
            alcohol=6.0,
            precio=55.00,
            importado=True,
        )

        repositorio.guardar()

        print(cerveza_nacional.descripcion())
        print(cerveza_importada.descripcion())

        # 3. CONSULTAS Y RELACIONES ENTRE OBJETOS.
        print("\n=== CONSULTAS DE OBJETOS ===")

        producto_consulta = repositorio.crear_producto(
            nombre="Cerveza Consulta Demo",
            marca="Frija",
            categoria="ConsultaTest",
            presentacion="Lata",
            contenido_ml=355,
            alcohol=4.5,
            precio=38.00,
        )

        inventario_consulta = repositorio.crear_inventario(
            sucursal="Tijuana",
            producto_id=producto_consulta.producto_id,
            stock=2,
            stock_minimo=5,
        )

        envio_consulta = repositorio.crear_envio(
            cliente="Cliente de prueba",
            sucursal="Tijuana",
            direccion="Tijuana, Baja California",
        )

        repositorio.agregar_producto_envio(
            envio_id=envio_consulta.envio_id,
            producto_id=producto_consulta.producto_id,
            cantidad=3,
        )

        repositorio.guardar()

        productos_categoria = repositorio.productos_por_categoria(
            "ConsultaTest"
        )
        inventarios_bajos = repositorio.inventario_bajo()
        envios_pendientes = repositorio.envios_pendientes()

        print("Productos por categoría:", len(productos_categoria))
        print("Inventarios bajos:", len(inventarios_bajos))
        print("Envíos pendientes:", len(envios_pendientes))

        print("Descripción del envío:", envio_consulta.descripcion())

        if envio_consulta.detalles:
            detalle = envio_consulta.detalles[0]
            print(
                "Producto del detalle:",
                detalle["producto"].descripcion(),
            )

        # 4. ELIMINACIÓN DE UN ENVÍO Y SUS DETALLES.
        print("\n=== ELIMINACIÓN EN CASCADA ===")

        id_envio_prueba = envio_consulta.envio_id

        resultado = repositorio.eliminar_envio(id_envio_prueba)

        print("ELIMINACIÓN EN CASCADA:", resultado)
        print("DETALLES RESTANTES:", len(envio_consulta.detalles))

        if not resultado or len(envio_consulta.detalles) != 0:
            raise AssertionError("Falló la eliminación del envío o sus detalles.")

        repositorio.guardar()

        # 5. VALIDACIONES.
        probar_validaciones(repositorio)

        print("\nTodas las pruebas finalizaron correctamente.")

    finally:
        try:
            if repositorio is not None:
                repositorio.cerrar()
        finally:
            # Eliminar solamente el archivo temporal de esta ejecución.
            if os.path.exists(ruta_temporal):
                os.remove(ruta_temporal)


if __name__ == "__main__":
    main()
