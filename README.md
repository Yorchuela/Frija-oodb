# Frija Brewery

## Sistema de gestión de una distribuidora de cerveza

### 1. Descripción del proyecto

Yorch-Asociados es un proyecto desarrollado en Python que simula la gestión de una distribuidora de cerveza llamada Frija. Utiliza Durus para almacenar objetos y conservar la información del sistema.

El proyecto permite administrar productos, inventarios y envíos, aplicando conceptos de programación orientada a objetos y persistencia de datos.

### 2. Objetivo

Implementar un sistema de gestión que permita realizar operaciones sobre productos, inventarios y envíos mediante una base de datos orientada a objetos, aplicando herencia, polimorfismo, relaciones entre objetos y transacciones.

### 3. Tecnologías utilizadas

- **Python:** desarrollo de la lógica del sistema.
- **Durus:** almacenamiento y persistencia de objetos.
- **Git y GitHub:** control de versiones y administración del repositorio.

### 4. Estructura del proyecto

- **`main.py`:** ejecuta las operaciones principales y las pruebas del sistema.
- **`models.py`:** contiene las clases del proyecto, sus atributos, métodos y validaciones.
- **`repository.py`:** administra las operaciones de persistencia, consultas y transacciones.
- **`requirements.txt`:** especifica las dependencias del proyecto.
- **`data/`:** almacena los archivos de datos generados localmente.

### 5. Modelos implementados

**Producto:** representa una cerveza e incluye información como nombre, marca, categoría, presentación, contenido, porcentaje de alcohol y precio.

**CervezaNacional y CervezaImportada:** clases derivadas de `Producto` que permiten aplicar herencia y polimorfismo mediante descripciones especializadas.

**Inventario:** administra las existencias de productos por sucursal y permite identificar niveles bajos de stock.

**Envío:** representa los envíos a clientes e incluye su destino, estado y los productos asociados.

### 6. Funcionalidades

- Crear, consultar, actualizar y eliminar productos.
- Registrar y administrar inventarios.
- Relacionar productos con sus inventarios.
- Registrar envíos y asociar productos con cantidades.
- Consultar productos por categoría.
- Identificar inventarios con existencias bajas.
- Consultar envíos pendientes.
- Aplicar transacciones para confirmar o revertir cambios.
- Validar los datos antes de almacenarlos.
- Cerrar el repositorio de forma segura.

### 7. Pruebas realizadas

Se realizaron pruebas para comprobar el funcionamiento de las operaciones y el manejo de errores.

- **CRUD:** verificación de las operaciones de creación, consulta, actualización y eliminación.
- **Relaciones entre objetos:** comprobación de las referencias entre productos, inventarios y envíos.
- **Herencia y polimorfismo:** verificación de las descripciones de cervezas nacionales e importadas.
- **Transacciones:** comprobación de `COMMIT` para confirmar cambios y `ABORT` para revertirlos.
- **Validaciones:** seis pruebas para rechazar precios negativos, porcentajes de alcohol inválidos, contenido infinito, existencias negativas, productos inexistentes y categorías vacías.
- **Cierre del repositorio:** comprobación de que no se permitan operaciones después del cierre y de que cerrarlo dos veces sea seguro.

**Resultado:** en la última ejecución, las seis pruebas de validación fueron aprobadas y el programa finalizó correctamente.

### 8. Conclusión

El proyecto permitió aplicar conceptos de programación orientada a objetos y persistencia de datos mediante Python y Durus. Se implementaron operaciones de administración, relaciones entre objetos, herencia, polimorfismo, transacciones y validaciones, comprobando su funcionamiento mediante pruebas.

