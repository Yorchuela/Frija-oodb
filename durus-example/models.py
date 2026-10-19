
from durus.persistent import Persistent
from durus.persistent_list import PersistentList
from durus.persistent_dict import PersistentDict


class Producto(Persistent):
    """Representa un producto de la cervecería."""

    def __init__(
        self,
        producto_id,
        nombre,
        marca,
        categoria,
        presentacion,
        contenido_ml,
        alcohol,
        precio,
    ):
        self.producto_id = producto_id
        self._nombre = nombre
        self._marca = marca
        self._categoria = categoria
        self._presentacion = presentacion
        self._contenido_ml = contenido_ml
        self._alcohol = alcohol
        self._precio = precio

        self.validar_datos()

    def validar_datos(self):
        """Valida los datos iniciales del producto."""

        if not isinstance(self._nombre, str) or not self._nombre.strip():
            raise ValueError("El nombre es obligatorio.")

        if not isinstance(self._marca, str) or not self._marca.strip():
            raise ValueError("La marca es obligatoria.")

        if not isinstance(self._categoria, str) or not self._categoria.strip():
            raise ValueError("La categoría es obligatoria.")

        if (
            not isinstance(self._presentacion, str)
            or not self._presentacion.strip()
        ):
            raise ValueError("La presentación es obligatoria.")

        if (
            not isinstance(self._contenido_ml, (int, float))
            or isinstance(self._contenido_ml, bool)
            or self._contenido_ml <= 0
        ):
            raise ValueError("El contenido debe ser un número mayor que cero.")

        if (
            not isinstance(self._alcohol, (int, float))
            or isinstance(self._alcohol, bool)
            or not 0 <= self._alcohol <= 100
        ):
            raise ValueError("El alcohol debe estar entre 0 y 100.")

        if (
            not isinstance(self._precio, (int, float))
            or isinstance(self._precio, bool)
            or self._precio <= 0
        ):
            raise ValueError("El precio debe ser un número mayor que cero.")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor

    @property
    def marca(self):
        return self._marca

    @marca.setter
    def marca(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La marca no puede estar vacía.")
        self._marca = valor

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La categoría no puede estar vacía.")
        self._categoria = valor

    @property
    def presentacion(self):
        return self._presentacion

    @presentacion.setter
    def presentacion(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La presentación no puede estar vacía.")
        self._presentacion = valor

    @property
    def contenido_ml(self):
        return self._contenido_ml

    @contenido_ml.setter
    def contenido_ml(self, valor):
        if (
            not isinstance(valor, (int, float))
            or isinstance(valor, bool)
            or valor <= 0
        ):
            raise ValueError("El contenido debe ser un número mayor que cero.")
        self._contenido_ml = valor

    @property
    def alcohol(self):
        return self._alcohol

    @alcohol.setter
    def alcohol(self, valor):
        if (
            not isinstance(valor, (int, float))
            or isinstance(valor, bool)
            or not 0 <= valor <= 100
        ):
            raise ValueError("El alcohol debe estar entre 0 y 100.")
        self._alcohol = valor

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if (
            not isinstance(valor, (int, float))
            or isinstance(valor, bool)
            or valor <= 0
        ):
            raise ValueError("El precio debe ser un número mayor que cero.")
        self._precio = valor

    def descripcion(self):
        return (
            f"{self._nombre} | {self._marca} | "
            f"{self._presentacion} | ${self._precio:.2f}"
        )


class CervezaNacional(Producto):
    """Especialización para cerveza nacional."""

    def descripcion(self):
        return f"[NACIONAL] {super().descripcion()}"


class CervezaImportada(Producto):
    """Especialización para cerveza importada."""

    def descripcion(self):
        return f"[IMPORTADA] {super().descripcion()}"


class Inventario(Persistent):
    """Representa el inventario de un producto en una sucursal."""

    def __init__(
        self,
        inventario_id,
        sucursal,
        producto,
        stock,
        stock_minimo,
    ):
        if (
            not isinstance(stock, int)
            or isinstance(stock, bool)
            or not isinstance(stock_minimo, int)
            or isinstance(stock_minimo, bool)
            or stock < 0
            or stock_minimo < 0
        ):
            raise ValueError(
                "El stock y el stock mínimo deben ser enteros no negativos."
            )

        self.inventario_id = inventario_id
        self.sucursal = sucursal
        self.producto = producto
        self._stock = stock
        self._stock_minimo = stock_minimo

    @property
    def stock(self):
        return self._stock

    def agregar_stock(self, cantidad):
        if (
            not isinstance(cantidad, int)
            or isinstance(cantidad, bool)
            or cantidad <= 0
        ):
            raise ValueError("La cantidad debe ser un entero mayor que cero.")

        self._stock += cantidad

    def retirar_stock(self, cantidad):
        if (
            not isinstance(cantidad, int)
            or isinstance(cantidad, bool)
            or cantidad <= 0
        ):
            raise ValueError("La cantidad debe ser un entero mayor que cero.")

        if cantidad > self._stock:
            raise ValueError("No hay suficiente inventario.")

        self._stock -= cantidad

    def necesita_reabastecimiento(self):
        return self._stock <= self._stock_minimo


class Envio(Persistent):
    """Representa un envío de productos."""

    ESTADOS_VALIDOS = {
        "PENDING",
        "PREPARING",
        "SHIPPED",
        "DELIVERED",
        "CANCELLED",
    }

    def __init__(
        self,
        envio_id,
        cliente,
        sucursal,
        direccion,
        estado="PENDING",
    ):
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("Estado de envío no válido.")

        self.envio_id = envio_id
        self.cliente = cliente
        self.sucursal = sucursal
        self.direccion = direccion
        self.estado = estado
        self.detalles = PersistentList()

    def agregar_producto(self, producto, cantidad):
        if (
            not isinstance(cantidad, int)
            or isinstance(cantidad, bool)
            or cantidad <= 0
        ):
            raise ValueError("La cantidad debe ser un entero mayor que cero.")

        detalle = PersistentDict({
            "producto": producto,
            "cantidad": cantidad,
        })

        self.detalles.append(detalle)

    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            raise ValueError("Estado de envío no válido.")

        self.estado = nuevo_estado

    def descripcion(self):
        return (
            f"Envío #{self.envio_id} | "
            f"Destino: {self.direccion} | "
            f"Estado: {self.estado} | "
            f"Productos: {len(self.detalles)}"
        )
