
import math
import os
import tempfile

from repository import RepositorioCerveceria
from models import Producto


RUTA_PRUEBAS = os.path.join("data", "cerveceria_pruebas.durus")


def comprobar(condicion, mensaje):
    """Detiene las pruebas si una condición no se cumple."""
    if not condicion:
        raise AssertionError(mensaje)

    print(f"OK: {mensaje}")


def probar_validaciones():
    print("\n=== PRUEBAS DE VALIDACIÓN ===")

    total = 0

    def probar(nombre, accion):
        nonlocal total

        try:
            accion()
        except (ValueError, TypeError):
            print(f"OK: {nombre}")
            total += 1
        else:
            raise AssertionError(
                f"La validación no rechazó el caso: {nombre}"
            )

    probar(
        "se rechazó el precio negativo",
        lambda: Producto(
            None, "Cerveza", "Frija", "Prueba",
            "Botella", 355, 5.0, -10
        ),
    )

    probar(
        "se rechazó el porcentaje de alcohol inválido",
        lambda: Producto(
            None, "Cerveza", "Frija", "Prueba",
            "Botella", 355, 101, 40
        ),
    )

    probar(
        "se rechazó el contenido infinito",
        lambda: Producto(
            None, "Cerveza", "Frija", "Prueba",
            "Botella", math.inf, 5.0, 40
        ),
    )

    repositorio = RepositorioCerveceria(
        os.path.join("data", "validaciones_temporal.durus")
    )

    try:
        probar(
            "se rechazó el stock negativo",
            lambda: repositorio.crear_inventario(
                "Tijuana", 999999, -1, 5
            ),
        )

        probar(
            "se rechazó el producto inexistente",
            lambda: repositorio.crear_inventario(
                "Tijuana", 999999, 10, 5
            ),
        )

        probar(
            "se rechazó la categoría vacía",
            lambda: repositorio.productos_por_categoria("   "),
        )

    finally:
        repositorio.cerrar()

    print(
        f"\nResultado: {total}/6 pruebas de validación correctas."
    )

    comprobar(
        total == 6,
        "todas las validaciones rechazaron los datos incorrectos",
    )


def probar_cierre_repositorio():
    print("\n=== PRUEBA DE CIERRE DEL REPOSITORIO ===")

    os.makedirs("data", exist_ok=True)

    descriptor, ruta_temporal = tempfile.mkstemp(
        prefix="prueba_cierre_",
        suffix=".durus",
        dir="data",
    )
    os.close(descriptor)
    os.remove(ruta_temporal)

    repositorio = None

    try:
        repositorio = RepositorioCerveceria(ruta_temporal)

        # El repositorio debe funcionar antes del cierre.
        repositorio.listar_productos()

        comprobar(
            not repositorio.cerrado,
            "el repositorio está abierto inicialmente",
        )

        # Cerrar y comprobar el estado.
        repositorio.cerrar()

        comprobar(
            repositorio.cerrado,
            "el repositorio se cerró correctamente",
        )

        # Las operaciones deben rechazarse después del cierre.
        try:
            repositorio.listar_productos()
        except RuntimeError:
            print(
                "OK: se rechazó una operación después del cierre."
            )
        else:
            raise AssertionError(
                "Se permitió listar productos después del cierre."
            )

        # Cerrar por segunda vez no debe producir errores.
        repositorio.cerrar()

        print(
            "OK: cerrar el repositorio dos veces es seguro."
        )

    finally:
        if repositorio is not None:
            repositorio.cerrar()

        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)


def main():
    print("=== PRUEBA CRUD Y TRANSACCIONES ===")

    repositorio = RepositorioCerveceria(RUTA_PRUEBAS)

    try:
        # 1. CREATE
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

        # 2. READ
        producto_leido = repositorio.obtener_producto(
            producto.producto_id
        )

        comprobar(
            producto_leido is not None,
            "el producto creado se puede consultar",
        )

        print("READ:", producto_leido.descripcion())

        # 3. UPDATE
        precio_anterior = producto.precio

        comprobar(
            repositorio.actualizar_precio(
                producto.producto_id, 45.00
            ),
            "se actualizó el precio del producto",
        )

        producto_actualizado = repositorio.obtener_producto(
            producto.producto_id
        )

        print(
            f"UPDATE: precio de ${precio_anterior:.2f} "
            f"a ${producto_actualizado.precio:.2f}"
        )

        repositorio.guardar()

        # 4. INVENTARIO Y RELACIÓN CON EL PRODUCTO
        inventario = repositorio.crear_inventario(
            sucursal="Tijuana",
            producto_id=producto.producto_id,
            stock=10,
            stock_minimo=5,
        )

        repositorio.guardar()

        comprobar(
            inventario.producto.producto_id == producto.producto_id,
            "el inventario referencia al producto correcto",
        )

        print(
            f"RELACIÓN: inventario {inventario.inventario_id} "
            f"referencia al producto {inventario.producto.producto_id}."
        )

        # 5. DELETE INVENTARIO Y PRODUCTO
        comprobar(
            repositorio.eliminar_inventario(
                inventario.inventario_id
            ),
            "se eliminó el inventario",
        )

        repositorio.guardar()

        comprobar(
            repositorio.eliminar_producto(producto.producto_id),
            "se eliminó el producto",
        )

        repositorio.guardar()

        # 6. COMMIT
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

        comprobar(
            repositorio.obtener_producto(id_commit) is not None,
            "COMMIT conservó el producto confirmado",
        )

        # 7. ABORT
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

        comprobar(
            repositorio.obtener_producto(id_temporal) is None,
            "ABORT revirtió el producto temporal",
        )

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

        comprobar(
            "[NACIONAL]" in cerveza_nacional.descripcion(),
            "la cerveza nacional usa su descripción especializada",
        )

        comprobar(
            "[IMPORTADA]" in cerveza_importada.descripcion(),
            "la cerveza importada usa su descripción especializada",
        )

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

        comprobar(
            any(
                p.producto_id == producto_consulta.producto_id
                for p in productos_categoria
            ),
            "la consulta encuentra el producto por categoría",
        )

        comprobar(
            any(
                i.inventario_id == inventario_consulta.inventario_id
                for i in inventarios_bajos
            ),
            "la consulta encuentra el inventario bajo",
        )

        comprobar(
            any(
                e.envio_id == envio_consulta.envio_id
                for e in envios_pendientes
            ),
            "la consulta encuentra el envío pendiente",
        )

        print("\n=== ELIMINACIÓN DE ENVÍO Y DETALLES ===")

        comprobar(
            repositorio.eliminar_envio(envio_consulta.envio_id),
            "se eliminó el envío",
        )

        comprobar(
            len(envio_consulta.detalles) == 0,
            "el envío eliminado ya no conserva detalles",
        )

        repositorio.guardar()

    finally:
        repositorio.cerrar()

    probar_validaciones()
    probar_cierre_repositorio()

    print("\nTodas las pruebas finalizaron correctamente.")


if __name__ == "__main__":
    main()
