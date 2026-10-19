
import os

from durus.file_storage import FileStorage
from durus.connection import Connection
from durus.persistent_dict import PersistentDict

from models import (
    CervezaNacional,
    CervezaImportada,
    Inventario,
    Envio,
)


class RepositorioCerveceria:
    """Administra los objetos persistentes de la cervecería."""

    def __init__(self, ruta="data/cerveceria.durus"):
        directorio = os.path.dirname(ruta)

        if directorio:
            os.makedirs(directorio, exist_ok=True)

        self.storage = FileStorage(ruta)
        self.connection = Connection(self.storage)
        self.root = self.connection.get_root()
        self.cerrado = False

        # Colecciones persistentes principales.
        for nombre in ("productos", "inventarios", "envios"):
            if nombre not in self.root:
                self.root[nombre] = PersistentDict()

        # Contadores persistentes para no repetir identificadores.
        if "contadores" not in self.root:
            self.root["contadores"] = PersistentDict({
                "producto": 1,
                "inventario": 1,
                "envio": 1,
            })

        self.connection.commit()

    def _nuevo_id(self, tipo):
        identificador = self.root["contadores"][tipo]
        self.root["contadores"][tipo] = identificador + 1
        return identificador

    # ---------------- PRODUCTOS ----------------

    def crear_producto(
        self,
        nombre,
        marca,
        categoria,
        presentacion,
        contenido_ml,
        alcohol,
        precio,
        importado=False,
    ):
        producto_id = self._nuevo_id("producto")

        clase = CervezaImportada if importado else CervezaNacional

        producto = clase(
            producto_id,
            nombre,
            marca,
            categoria,
            presentacion,
            contenido_ml,
            alcohol,
            precio,
        )

        self.root["productos"][producto_id] = producto
        return producto

    def obtener_producto(self, producto_id):
        return self.root["productos"].get(producto_id)

    def listar_productos(self):
        return list(self.root["productos"].values())

    def actualizar_precio(self, producto_id, nuevo_precio):
        producto = self.obtener_producto(producto_id)

        if producto is None:
            return False

        producto.precio = nuevo_precio
        return True

    def eliminar_producto(self, producto_id):
        producto = self.obtener_producto(producto_id)

        if producto is None:
            return False

        # Evita eliminar productos que aún tienen inventario.
        for inventario in self.root["inventarios"].values():
            if inventario.producto.producto_id == producto_id:
                raise ValueError(
                    "No se puede eliminar: el producto tiene inventario."
                )

        # Evita dejar referencias a productos inexistentes en los envíos.
        for envio in self.root["envios"].values():
            for detalle in envio.detalles:
                if detalle["producto"].producto_id == producto_id:
                    raise ValueError(
                        "No se puede eliminar: el producto está "
                        "referenciado en un envío."
                    )

        del self.root["productos"][producto_id]
        return True

    # ---------------- INVENTARIO ----------------

    def crear_inventario(
        self,
        sucursal,
        producto_id,
        stock,
        stock_minimo,
    ):
        producto = self.obtener_producto(producto_id)

        if producto is None:
            raise ValueError("El producto no existe.")

        inventario_id = self._nuevo_id("inventario")

        inventario = Inventario(
            inventario_id,
            sucursal,
            producto,
            stock,
            stock_minimo,
        )

        self.root["inventarios"][inventario_id] = inventario
        return inventario

    def listar_inventario(self):
        return list(self.root["inventarios"].values())

    def eliminar_inventario(self, inventario_id):
        if inventario_id not in self.root["inventarios"]:
            return False

        del self.root["inventarios"][inventario_id]
        return True

    # ---------------- ENVÍOS ----------------

    def crear_envio(self, cliente, sucursal, direccion):
        envio_id = self._nuevo_id("envio")

        envio = Envio(
            envio_id,
            cliente,
            sucursal,
            direccion,
        )

        self.root["envios"][envio_id] = envio
        return envio

    def agregar_producto_envio(
        self,
        envio_id,
        producto_id,
        cantidad,
    ):
        envio = self.root["envios"].get(envio_id)
        producto = self.obtener_producto(producto_id)

        if envio is None:
            raise ValueError("El envío no existe.")

        if producto is None:
            raise ValueError("El producto no existe.")

        envio.agregar_producto(producto, cantidad)

    def listar_envios(self):
        return list(self.root["envios"].values())

    def cambiar_estado_envio(self, envio_id, estado):
        envio = self.root["envios"].get(envio_id)

        if envio is None:
            return False

        envio.cambiar_estado(estado)
        return True

    def eliminar_envio(self, envio_id):
        envio = self.root["envios"].get(envio_id)

        if envio is None:
            return False

        # Elimina los detalles antes de eliminar el envío.
        while len(envio.detalles) > 0:
            del envio.detalles[-1]

        del self.root["envios"][envio_id]
        return True

    # ---------------- CONSULTAS ----------------

    def productos_por_categoria(self, categoria):
        categoria_buscada = categoria.strip().casefold()

        return [
            producto
            for producto in self.root["productos"].values()
            if producto.categoria.casefold() == categoria_buscada
        ]

    def inventario_bajo(self):
        return [
            inventario
            for inventario in self.root["inventarios"].values()
            if inventario.necesita_reabastecimiento()
        ]

    def envios_pendientes(self):
        return [
            envio
            for envio in self.root["envios"].values()
            if envio.estado in ("PENDING", "PREPARING")
        ]

    # ---------------- TRANSACCIONES ----------------

    def guardar(self):
        """Confirma los cambios pendientes."""
        if self.cerrado:
            raise RuntimeError("El repositorio ya está cerrado.")

        self.connection.commit()

    def deshacer_cambios(self):
        """Revierte los cambios pendientes de la transacción actual."""
        if self.cerrado:
            raise RuntimeError("El repositorio ya está cerrado.")

        self.connection.abort()
        self.root = self.connection.get_root()

    def cerrar(self):
        """Confirma los cambios pendientes y cierra el almacenamiento."""
        if self.cerrado:
            return

        try:
            self.connection.commit()
        finally:
            self.storage.close()
            self.cerrado = True
