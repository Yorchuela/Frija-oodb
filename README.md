# Sistema de Base de Datos Orientada a Objetos para una Cervecería

## Descripción

Este proyecto implementa un ejemplo de base de datos orientada a objetos utilizando Python y Durus. Está basado en el sistema de una empresa dedicada a la distribución y exportación de cerveza.

El objetivo es representar productos, inventarios y envíos mediante objetos persistentes, permitiendo almacenar información, establecer referencias entre objetos y realizar operaciones de consulta y modificación.

## Tecnologías utilizadas

- Python 3
- Durus 4.3
- pywin32 (para la ejecución de Durus en Windows)
- Git y GitHub

## Estructura del proyecto

```text
Yorch-Asociados/
├── .gitignore
├── README.md
├── durus-example/
│   ├── main.py
│   ├── models.py
│   ├── repository.py
│   └── requirements.txt
└── venv/
```

La carpeta `venv` es el entorno virtual local y no debe subirse al repositorio.

## Modelos implementados

- **Producto:** representa una cerveza e incluye atributos, validaciones y métodos para consultar su descripción.
- **CervezaNacional:** especialización de Producto mediante herencia.
- **CervezaImportada:** especialización de Producto mediante herencia y polimorfismo.
- **Inventario:** mantiene una referencia al producto y administra las existencias.
- **Envio:** representa un envío y contiene una lista persistente de productos y cantidades.

## Instalación

Se requiere tener Python instalado.

Desde la terminal, ubicada en la carpeta raíz del proyecto, ejecutar:

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install -r durus-example/requirements.txt
```

## Ejecución

Desde la raíz del proyecto, ejecutar:

```bash
cd durus-example
python main.py
```

El programa ejecuta una prueba de transacciones para comprobar que `commit()` conserva los cambios confirmados y que `abort()` deshace los cambios pendientes.

## Persistencia

Durus almacena los objetos en un archivo propio. El repositorio administra las colecciones persistentes de productos, inventarios y envíos mediante `connection.get_root()`.

El método `commit()` confirma los cambios y `abort()` permite deshacer los cambios de la transacción actual.

## Relación con el modelo relacional

El ejemplo toma como referencia el sistema de distribución de cerveza que utiliza una base de datos relacional. Las clases de Python representan conceptos del negocio y utilizan referencias entre objetos en lugar de depender exclusivamente de claves foráneas y operaciones JOIN.

## Autoría y propósito académico

Proyecto académico para la asignatura Tópicos de Bases de Datos. Su propósito es estudiar las bases de datos orientadas a objetos, la persistencia, la herencia, el polimorfismo y las relaciones entre objetos.
