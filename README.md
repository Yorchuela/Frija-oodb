# Yorch-Asociados

## Sistema de gestión de una distribuidora de cerveza con base de datos orientada a objetos

## Descripción del proyecto

Este proyecto consiste en el desarrollo de un sistema para gestionar información de una distribuidora de cerveza llamada **Frija**, utilizando bases de datos orientadas a objetos.

El proyecto permite administrar productos, inventarios y envíos mediante clases de Python y el sistema de persistencia de objetos Durus. También implementa relaciones entre objetos, herencia, polimorfismo y manejo de transacciones.

## Objetivo

Implementar y probar las operaciones principales de un sistema de gestión de una distribuidora de cerveza utilizando Python y una base de datos orientada a objetos.

## Tecnologías utilizadas

- **Python:** lenguaje de programación.
- **Durus:** almacenamiento y persistencia de objetos Python.
- **PowerShell:** ejecución de comandos y administración del entorno de desarrollo.
- **Git y GitHub:** control de versiones y respaldo del código fuente.

## Estructura del proyecto

```text
Yorch-Asociados/
├── durus-example/
│   ├── data/
│   ├── main.py
│   ├── models.py
│   ├── repository.py
│   └── requirements.txt
├── .gitignore
└── README.md
```

**Descripción de los archivos principales:**

- `main.py`: ejecuta las operaciones del sistema y las pruebas.
- `models.py`: contiene las clases y validaciones de los objetos.
- `repository.py`: administra la persistencia, las consultas y las operaciones sobre los objetos.
- `requirements.txt`: contiene las dependencias necesarias.
- `data/`: almacena los archivos de datos generados localmente.

## Modelos del sistema

### Producto

Representa una cerveza y almacena información como nombre, marca, categoría, presentación, contenido en mililitros, porcentaje de alcohol y precio.

Se utilizan las clases `CervezaNacional` y `CervezaImportada`, derivadas de `Producto`, para demostrar herencia y polimorfismo.

### Inventario

Permite registrar las existencias de un producto por sucursal y establecer un nivel mínimo de stock para identificar cuándo es necesario reabastecer.

### Envío

Representa un envío a un cliente e incluye la sucursal de origen, la dirección de destino, el estado del envío y los productos asociados.

## Funcionalidades implementadas

- Crear, consultar, actualizar y eliminar productos.
- Registrar y eliminar inventarios.
- Relacionar productos con inventarios.
- Registrar envíos y asociar productos con sus cantidades.
- Consultar productos por categoría.
- Identificar inventarios con existencias bajas.
- Consultar envíos pendientes.
- Utilizar herencia y polimorfismo en los tipos de cerveza.
- Confirmar cambios mediante `COMMIT`.
- Revertir cambios mediante `ABORT`.
- Validar los datos antes de almacenarlos.
- Cerrar el repositorio de forma segura e impedir operaciones posteriores al cierre.

## Validaciones implementadas

El sistema comprueba que los datos sean válidos antes de crear o modificar objetos. Entre las validaciones probadas se encuentran:

- Rechazo de precios negativos.
- Rechazo de porcentajes de alcohol fuera del rango permitido.
- Rechazo de contenido infinito.
- Rechazo de existencias negativas.
- Rechazo de referencias a productos inexistentes.
- Rechazo de categorías vacías.

## Requisitos previos

Para ejecutar el proyecto se necesita:

- Python instalado.
- Git, si se desea clonar el repositorio.
- Un entorno virtual de Python.
- Las dependencias indicadas en `durus-example/requirements.txt`.

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Yorchuela/Frija-oodb.git
cd Frija-oodb
```

### 2. Crear el entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

En Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución del script, se puede habilitar temporalmente para la sesión actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Después, activar nuevamente el entorno virtual.

### 4. Instalar las dependencias

Desde la raíz del proyecto:

```powershell
pip install -r durus-example/requirements.txt
```

## Ejecución del sistema

Desde la raíz del repositorio, ejecutar:

```powershell
cd durus-example
python main.py
```

El programa realiza operaciones de prueba sobre productos, inventarios y envíos, además de ejecutar las pruebas de validación y cierre del repositorio.

## Ejecución de las pruebas

Desde la carpeta `durus-example`, ejecutar primero:

```powershell
python -m py_compile models.py repository.py main.py
```

Este comando comprueba que los archivos no contengan errores de sintaxis.

Después, ejecutar:

```powershell
python main.py
```

El programa muestra los resultados de las operaciones y de las pruebas implementadas.

### Pruebas realizadas

| Prueba | Resultado esperado |
|---|---|
| CRUD de productos | Operaciones ejecutadas correctamente |
| Relaciones entre objetos | Referencias verificadas |
| Herencia y polimorfismo | Descripciones especializadas verificadas |
| Consultas | Productos, inventarios y envíos encontrados |
| COMMIT | Cambios confirmados y conservados |
| ABORT | Cambios temporales revertidos |
| Validaciones | 6 de 6 pruebas aprobadas |
| Cierre del repositorio | Operaciones posteriores al cierre rechazadas |

**Resultado obtenido:** todas las pruebas finalizaron correctamente en la última ejecución realizada.

## Persistencia de los datos

Durus permite conservar los objetos en archivos de almacenamiento local. Los archivos de datos se generan durante la ejecución y se mantienen dentro de la carpeta `data/`.

Los archivos de datos locales no forman parte del código fuente que debe compartirse en GitHub. Por ello, la carpeta se excluye mediante `.gitignore`.

## Control de versiones

El proyecto utiliza Git para registrar los cambios realizados durante el desarrollo y GitHub para alojar el repositorio remoto.

Los cambios se pueden registrar y publicar con los siguientes comandos, ejecutados desde la raíz del repositorio:

```bash
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

## Conclusión

El proyecto permite aplicar conceptos de programación orientada a objetos y persistencia de datos en Python. Las pruebas realizadas verifican las operaciones principales, las relaciones entre objetos, las transacciones, las validaciones y el cierre seguro del repositorio.

Este desarrollo constituye una base funcional para continuar ampliando el sistema de gestión de una distribuidora de cerveza.
