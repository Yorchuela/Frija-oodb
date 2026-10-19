
import math

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

    @staticmethod
    def _validar_texto(valor, campo):
        """Comprueba que un texto no esté vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{campo} es obligatorio.")

    @staticmethod
    def _validar_numero(valor, campo, minimo=None, maximo=None):
        """Valida números finitos y sus límites."""
        if (
            not isinstance(valor, (int, float))
            or isinstance(valor, bool)
            or not math.isfinite(valor)
        ):
            raise ValueError(f"{campo} debe ser un número finito.")

        if minimo is not None and valor < minimo:
            raise ValueError(f"{campo} debe ser mayor o igual a {minimo}.")

        if maximo is not None and valor > maximo:
            raise ValueError(f"{campo} debe ser menor o igual a {maximo}.")

    def validar_datos(self):
        """Valida los datos iniciales del producto."""
        self._validar_texto(self._nombre, "El nombre")
        self._validar_texto(self._marca, "La marca")
        self._validar_texto(self._categoria, "La categoría")
        self._validar_texto(self._presentacion, "La presentación")

        self._validar_numero(
            self._contenido_ml, "El contenido", minimo=0
        )
        if self._contenido_ml == 0:
            raise ValueError("El contenido debe ser mayor que cero.")

        self._validar_numero(
            self._alcohol, "El porcentaje de alcohol", minimo=0, maximo=100
        )

        self._validar_numero(self._precio, "El precio", minimo=0)
        if self._precio == 0:
            raise ValueError("El precio debe ser mayor que cero.")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._validar_texto(valor, "El nombre")
        self._nombre = valor

    @property
    def marca(self):
        return self._marca

    @marca.setter
    def marca(self, valor):
        self._validar_texto(valor, "La marca")
        self._marca = valor

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        self._validar_texto(valor, "La categoría")
        self._categoria = valor

    @property
    def presentacion(self):
        return self._presentacion

    @presentacion.setter
    def presentacion(self, valor):
        self._validar_texto(valor, "La presentación")
        self._presentacion = valor

    @property
    def contenido_ml(self):
        return self._contenido_ml

    @contenido_ml.setter
    def contenido_ml(self, valor):
        self._validar_numero(valor, "El contenido", minimo=0)
        if valor == 0:
            raise ValueError("El contenido debe ser mayor que cero.")
        self._contenido_ml = valor

    @property
    def alcohol(self):
        return self._alcohol

    @alcohol.setter
    def alcohol(self, valor):
        self._validar_numero(
            valor, "El porcentaje de alcohol", minimo=0, maximo=100
        )
        self._alcohol = valor

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        self._validar_numero(valor, "El precio", minimo=0)
        if valor == 0:
            raise ValueError("El precio debe ser mayor que cero.")
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
        self._validar_entero_no_negativo(stock, "El stock")
        self._validar_entero_no_negativo(stock_minimo, "El stock mínimo")

        if not isinstance(sucursal, str) or not sucursal.strip():
            raise ValueError("La sucursal es obligatoria.")

        if not isinstance(producto, Producto):
            raise ValueError("El producto debe ser un objeto Producto válido.")

        self.inventario_id = inventario_id
        self.sucursal = sucursal
        self.producto = producto
        self._stock = stock
        self._stock_minimo = stock_minimo

    @staticmethod
    def _validar_entero_no_negativo(valor, campo):
        if (
            not isinstance(valor, int)
            or isinstance(valor, bool)
            or valor < 0
        ):
            raise ValueError(
                f"{campo} debe ser un entero no negativo."
            )

    @property
    def stock(self):
        return self._stock

    @property
    def stock_minimo(self):
        return self._stock_minimo

    def agregar_stock(self, cantidad):
        if (
            not isinstance(cantidad, int)
            or isinstance(cantidad, bool)
            or cantidad <= 0
        ):
            raise ValueError(
                "La cantidad debe ser un entero mayor que cero."
            )

        self._stock += cantidad

    def retirar_stock(self, cantidad):
        if (
            not isinstance(cantidad, int)
            or isinstance(cantidad, bool)
            or cantidad <= 0
        ):
            raise ValueError(
                "La cantidad debe ser un entero mayor que cero."
            )

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
        if not isinstance(cliente, str) or not cliente.strip():
            raise ValueError("El cliente es obligatorio.")

        if not isinstance(sucursal, str) or not sucursal.strip():
            raise ValueError("La sucursal es obligatoria.")

        if not isinstance(direccion, str) or not direccion.strip():
            raise ValueError("La dirección es obligatoria.")

        self._validar_estado(estado)

        self.envio_id = envio_id
        self.cliente = cliente
        self.sucursal = sucursal
        self.direccion = direccion
        self.estado = estado
        self.detalles = PersistentList()

    @classmethod
    def _validar_estado(cls, estado):
        if not isinstance(estado, str) or estado not in cls.ESTADOS_VALIDOS:
            raise ValueError("Estado de envío no válido.")

    def agregar_producto(self, producto, cantidad):
        if not isinstance(producto, Producto):
            raise ValueError("El producto debe ser un objeto Producto válido.")

        if (
            not isinstance(cantidad, int)
            or isinstance(cantidad, bool)
            or cantidad <= 0
        ):
            raise ValueError(
                "La cantidad debe ser un entero mayor que cero."
            )

        detalle = PersistentDict({
            "producto": producto,
            "cantidad": cantidad,
        })

        self.detalles.append(detalle)

    def cambiar_estado(self, nuevo_estado):
        self._validar_estado(nuevo_estado)
        self.estado = nuevo_estado

    def descripcion(self):
        return (
            f"Envío #{self.envio_id} | "
            f"Destino: {self.direccion} | "
            f"Estado: {self.estado} | "
            f"Productos: {len(self.detalles)}"
        )
