# Sistema de Base de Datos Orientada a Objetos para una Cervecería

## 1. Descripción

Este proyecto implementa un ejemplo de base de datos orientada a objetos utilizando Python y Durus. Está basado en el sistema de una empresa dedicada a la distribución y exportación de cerveza.

El objetivo es representar productos, inventarios y envíos mediante objetos persistentes, permitiendo almacenar información, establecer referencias entre objetos y realizar operaciones de consulta y modificación.

## 2. Tecnologías utilizadas

- Python 3
- Durus 4.3
- pywin32
- Git y GitHub

## 3. Estructura del proyecto

```text
Yorch-Asociados/
├── .gitignore
├── README.md
├── diagrama_clases.md
└── durus-example/
    ├── main.py
    ├── models.py
    ├── repository.py
    └── requirements.txt
```

La carpeta `venv` corresponde al entorno virtual local y no debe subirse al repositorio. La carpeta `data` almacena los archivos de persistencia generados durante la ejecución.

## 4. Modelos implementados

- **Producto:** representa una cerveza e incluye atributos, validaciones y métodos para consultar su descripción.
- **CervezaNacional:** especialización de `Producto` mediante herencia.
- **CervezaImportada:** especialización de `Producto` mediante herencia y polimorfismo.
- **Inventario:** mantiene una referencia al producto y administra las existencias de una sucursal.
- **Envio:** representa un envío y contiene una colección persistente de productos y cantidades.

## 5. Instalación

Se requiere tener Python instalado.

Desde la terminal, ubicada en la carpeta raíz del proyecto, ejecutar:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r .\durus-example\requirements.txt
```

Si PowerShell bloquea la activación del entorno virtual, ejecutar lo siguiente en esa misma terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

## 6. Ejecución

Desde la raíz del proyecto, ejecutar:

```powershell
cd .\durus-example
python main.py
```

El programa ejecuta pruebas de operaciones CRUD, relaciones entre objetos, herencia, polimorfismo, consultas y transacciones.

## 7. Persistencia y transacciones

Durus almacena los objetos en un archivo propio. El repositorio administra las colecciones persistentes de productos, inventarios y envíos mediante `connection.get_root()`.

El método `commit()` confirma los cambios realizados, mientras que `abort()` revierte los cambios pendientes de la transacción actual.

## 8. Relación con el modelo relacional

El proyecto toma como referencia el sistema de distribución de cerveza que utiliza una base de datos relacional. Las clases de Python representan conceptos del negocio y utilizan referencias entre objetos en lugar de depender exclusivamente de claves foráneas y operaciones `JOIN`.

## 9. Diagrama de clases

El archivo `diagrama_clases.md` contiene el diagrama UML del modelo orientado a objetos, incluyendo las clases principales, sus relaciones y la herencia.

## 10. Autoría y propósito académico

Proyecto académico para la asignatura Tópicos de Bases de Datos. Su propósito es estudiar las bases de datos orientadas a objetos, la persistencia, la herencia, el polimorfismo, las transacciones y las relaciones entre objetos.