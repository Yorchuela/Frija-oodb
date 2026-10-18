
classDiagram
    class Persistent {
        <<Durus>>
    }

    class Producto {
        +int producto_id
        -str nombre
        -str marca
        -str categoria
        -str presentacion
        -float contenido_ml
        -float alcohol
        -float precio
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
        -int stock
        -int stock_minimo
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
    Envio --> Producto : incluye productos
    Envio *-- "0..*" DetalleEnvio : contiene

    class DetalleEnvio {
        +Producto producto
        +int cantidad
    }
