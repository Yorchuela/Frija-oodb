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

        for nombre in ("productos", "inventarios", "envios"):
            if nombre not in self.root:
                self.root[nombre] = PersistentDict()

        if "contadores" not in self.root:
            self.root["contadores"] = PersistentDict({
                "producto": 1,
                "inventario": 1,
                "envio": 1,
            })

        self.connection.commit()

    def _comprobar_abierto(self):
        """Impide utilizar el repositorio después de cerrarlo."""
        if self.cerrado:
            raise RuntimeError("El repositorio ya está cerrado.")

    def _nuevo_id(self, tipo):
        self._comprobar_abierto()

        if tipo not in self.root["contadores"]:
            raise ValueError("Tipo de identificador no válido.")

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
        self._comprobar_abierto()

        if not isinstance(importado, bool):
            raise ValueError("El parámetro importado debe ser booleano.")

        # Validar antes de incrementar el contador.
        clase = CervezaImportada if importado else CervezaNacional

        producto = clase(
            None,
            nombre,
            marca,
            categoria,
            presentacion,
            contenido_ml,
            alcohol,
            precio,
        )

        producto.producto_id = self._nuevo_id("producto")
        self.root["productos"][producto.producto_id] = producto

        return producto

    def obtener_producto(self, producto_id):
        self._comprobar_abierto()
        return self.root["productos"].get(producto_id)

    def listar_productos(self):
        self._comprobar_abierto()
        return list(self.root["productos"].values())

    def actualizar_precio(self, producto_id, nuevo_precio):
        self._comprobar_abierto()

        producto = self.obtener_producto(producto_id)

        if producto is None:
            return False

        # El setter valida el precio antes de modificarlo.
        producto.precio = nuevo_precio

        return True

    def eliminar_producto(self, producto_id):
        self._comprobar_abierto()

        producto = self.obtener_producto(producto_id)

        if producto is None:
            return False

        for inventario in self.root["inventarios"].values():
            if inventario.producto.producto_id == producto_id:
                raise ValueError(
                    "No se puede eliminar: el producto tiene inventario."
                )

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
        self._comprobar_abierto()

        producto = self.obtener_producto(producto_id)

        if producto is None:
            raise ValueError("El producto no existe.")

        # Construir primero para validar los datos antes de asignar el ID.
        inventario = Inventario(
            None,
            sucursal,
            producto,
            stock,
            stock_minimo,
        )

        inventario.inventario_id = self._nuevo_id("inventario")
        self.root["inventarios"][inventario.inventario_id] = inventario

        return inventario

    def listar_inventario(self):
        self._comprobar_abierto()
        return list(self.root["inventarios"].values())

    def eliminar_inventario(self, inventario_id):
        self._comprobar_abierto()

        if inventario_id not in self.root["inventarios"]:
            return False

        del self.root["inventarios"][inventario_id]

        return True

    # ---------------- ENVÍOS ----------------

    def crear_envio(self, cliente, sucursal, direccion):
        self._comprobar_abierto()

        envio = Envio(
            None,
            cliente,
            sucursal,
            direccion,
        )

        envio.envio_id = self._nuevo_id("envio")
        self.root["envios"][envio.envio_id] = envio

        return envio

    def agregar_producto_envio(
        self,
        envio_id,
        producto_id,
        cantidad,
    ):
        self._comprobar_abierto()

        envio = self.root["envios"].get(envio_id)
        producto = self.obtener_producto(producto_id)

        if envio is None:
            raise ValueError("El envío no existe.")

        if producto is None:
            raise ValueError("El producto no existe.")

        envio.agregar_producto(producto, cantidad)

    def listar_envios(self):
        self._comprobar_abierto()
        return list(self.root["envios"].values())

    def cambiar_estado_envio(self, envio_id, estado):
        self._comprobar_abierto()

        envio = self.root["envios"].get(envio_id)

        if envio is None:
            return False

        envio.cambiar_estado(estado)

        return True

    def eliminar_envio(self, envio_id):
        self._comprobar_abierto()

        envio = self.root["envios"].get(envio_id)

        if envio is None:
            return False

        while len(envio.detalles) > 0:
            del envio.detalles[-1]

        del self.root["envios"][envio_id]

        return True

    # ---------------- CONSULTAS ----------------

    def productos_por_categoria(self, categoria):
        self._comprobar_abierto()

        if not isinstance(categoria, str) or not categoria.strip():
            raise ValueError("La categoría de búsqueda es obligatoria.")

        categoria_buscada = categoria.strip().casefold()

        return [
            producto
            for producto in self.root["productos"].values()
            if producto.categoria.casefold() == categoria_buscada
        ]

    def inventario_bajo(self):
        self._comprobar_abierto()

        return [
            inventario
            for inventario in self.root["inventarios"].values()
            if inventario.necesita_reabastecimiento()
        ]

    def envios_pendientes(self):
        self._comprobar_abierto()

        return [
            envio
            for envio in self.root["envios"].values()
            if envio.estado in ("PENDING", "PREPARING")
        ]

    # ---------------- TRANSACCIONES ----------------

    def guardar(self):
        """Confirma los cambios pendientes."""
        self._comprobar_abierto()
        self.connection.commit()

    def deshacer_cambios(self):
        """Revierte los cambios pendientes de la transacción actual."""
        self._comprobar_abierto()

        self.connection.abort()
        self.root = self.connection.get_root()

    def cerrar(self):
        """Confirma los cambios pendientes y cierra el almacenamiento."""
        if self.cerrado:
            return

        try:
            self.connection.commit()
        finally:
            try:
                self.storage.close()
            finally:
                self.cerrado = True
