
from repository import RepositorioCerveceria


def main():
    repositorio = RepositorioCerveceria()

    try:
        print("=== PRUEBA DE TRANSACCIONES ===")

        # 1. Crear un producto y confirmar los cambios.
        producto = repositorio.crear_producto(
            nombre="Cerveza para commit",
            marca="Prueba",
            categoria="Experimental",
            presentacion="Botella",
            contenido_ml=355,
            alcohol=5.0,
            precio=40.00,
        )

        repositorio.guardar()
        print("COMMIT: Producto guardado correctamente.")

        # 2. Crear otro producto y deshacer los cambios.
        producto_prueba = repositorio.crear_producto(
            nombre="Cerveza para abort",
            marca="Prueba",
            categoria="Experimental",
            presentacion="Lata",
            contenido_ml=473,
            alcohol=4.5,
            precio=35.00,
        )

        id_abort = producto_prueba.producto_id

        repositorio.deshacer_cambios()
        print("ABORT: Cambios deshechos.")

        # 3. Comprobar que el primer producto existe
        # y que el segundo no quedó guardado.
        producto_guardado = repositorio.obtener_producto(
            producto.producto_id
        )
        producto_desh_echo = repositorio.obtener_producto(id_abort)

        print(
            "Verificación commit:",
            "Producto conservado"
            if producto_guardado is not None
            else "Error"
        )

        print(
            "Verificación abort:",
            "Producto no guardado"
            if producto_desh_echo is None
            else "Error: el producto existe"
        )

    finally:
        repositorio.cerrar()


if __name__ == "__main__":
    main()
