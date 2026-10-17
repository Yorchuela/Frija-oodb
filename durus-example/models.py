
from durus.persistent import Persistent
from durus.persistent_list import PersistentList


class Producto(Persistent):
    """Representa un producto de la tabla products."""

    def __init__(
        self, producto_id, nombre, marca, categoria,
        presentacion, contenido_ml, alcohol, precio
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
        if not self._nombre.strip():
            raise ValueError("El nombre es obligatorio.")
        if self._contenido_ml <= 0:
            raise ValueError("El contenido debe ser mayor que cero.")
        if not 0 <= self._alcohol <= 100:
            raise ValueError("El alcohol debe estar entre 0 y 100.")
        if self._precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor <= 0:
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
    """Representa la tabla inventory."""

    def __init__(
        self, inventario_id, sucursal, producto, stock, stock_minimo
    ):
        if stock < 0 or stock_minimo < 0:
            raise ValueError("El stock no puede ser negativo.")

        self.inventario_id = inventario_id
        self.sucursal = sucursal
        self.producto = producto
        self._stock = stock
        self._stock_minimo = stock_minimo

    @property
    def stock(self):
        return self._stock

    def agregar_stock(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        self._stock += cantidad

    def retirar_stock(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        if cantidad > self._stock:
            raise ValueError("No hay suficiente inventario.")
        self._stock -= cantidad

    def necesita_reabastecimiento(self):
        return self._stock <= self._stock_minimo


class Envio(Persistent):
    """Representa la tabla shipments."""

    def __init__(
        self, envio_id, cliente, sucursal, direccion,
        estado="PENDING"
    ):
        self.envio_id = envio_id
        self.cliente = cliente
        self.sucursal = sucursal
        self.direccion = direccion
        self.estado = estado
        self.detalles = PersistentList()

    def agregar_producto(self, producto, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        self.detalles.append({
            "producto": producto,
            "cantidad": cantidad,
        })

    def cambiar_estado(self, nuevo_estado):
        estados_validos = {
            "PENDING", "PREPARING", "SHIPPED",
            "DELIVERED", "CANCELLED"
        }
        if nuevo_estado not in estados_validos:
            raise ValueError("Estado de envío no válido.")
        self.estado = nuevo_estado

    def descripcion(self):
        return (
            f"Envío #{self.envio_id} | "
            f"Destino: {self.direccion} | "
            f"Estado: {self.estado} | "
            f"Productos: {len(self.detalles)}"
        )
