```mermaid
classDiagram
    class Persistent {
        <<Durus>>
    }

    class PersistentList {
        <<Durus>>
    }

    class PersistentDict {
        <<Durus>>
    }

    class Producto {
        +int producto_id
        -str _nombre
        -str _marca
        -str _categoria
        -str _presentacion
        -float _contenido_ml
        -float _alcohol
        -float _precio
        +nombre
        +marca
        +categoria
        +presentacion
        +contenido_ml
        +alcohol
        +precio
        +validar_datos()
        +descripcion()
    }

    class CervezaNacional {
        +descripcion()
    }

    class CervezaImportada {
        +descripcion()
    }

    class Inventario {
        +int inventario_id
        +str sucursal
        +Producto producto
        -int _stock
        -int _stock_minimo
        +stock
        +agregar_stock(cantidad)
        +retirar_stock(cantidad)
        +necesita_reabastecimiento()
    }

    class Envio {
        +int envio_id
        +str cliente
        +str sucursal
        +str direccion
        +str estado
        +PersistentList detalles
        +agregar_producto(producto, cantidad)
        +cambiar_estado(nuevo_estado)
        +descripcion()
    }

    Persistent <|-- Producto
    Persistent <|-- Inventario
    Persistent <|-- Envio

    Producto <|-- CervezaNacional
    Producto <|-- CervezaImportada

    Inventario --> Producto : referencia
    Envio *-- PersistentList : detalles
    PersistentList *-- PersistentDict : elementos
    PersistentDict --> Producto : producto
    ```
