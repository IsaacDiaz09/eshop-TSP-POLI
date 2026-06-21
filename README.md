# Volt Athletics - Catálogo Virtual de Ropa Deportiva

Volt Athletics es una aplicación e-commerce premium de indumentaria y calzado deportivo. Este proyecto fue desarrollado bajo la metodología de ingeniería de software **TSPi (Team Software Process)** e integra PSP (Personal Software Process) para el control estadístico de calidad de software y esfuerzo del equipo.

La aplicación frontend + backend es completamente autónoma y se ejecuta localmente mediante **un único comando de Docker Compose**.

---

## 🛠️ Arquitectura y Tecnologías

El sistema está dividido en tres contenedores de Docker coordinados de forma segura:

1.  **Frontend (Nginx - Puerto 80)**:
    *   Desarrollado en **HTML5 y JavaScript Puro (Vanilla JS)**.
    *   Maquetación limpia, responsiva y consistente basada en **Bootstrap 5** (CSS e Iconos).
    *   Configurado como proxy inverso en Nginx para redirigir las rutas de API `/api/` y el panel `/admin/` al contenedor del backend, evitando problemas de CORS de manera nativa.
2.  **Backend (Django - Puerto 80)**:
    *   Servidor API REST construido con **Python 3.11**, **Django** y **Django REST Framework (DRF)**.
    *   Autenticación de sesiones protegida mediante **JSON Web Tokens (JWT)** con `djangorestframework-simplejwt`.
    *   Paginación automática del catálogo a razón de **9 elementos por página**.
3.  **Base de Datos (PostgreSQL - Puerto 5432)**:
    *   Persistencia de datos relacional para usuarios, categorías, productos, variantes y pedidos mediante un volumen de Docker (`postgres_data`).

---

## 🚀 Módulos Funcionales Implementados

*   **Registro e Inicio de Sesión**: Validación de credenciales cifradas y persistencia de tokens de sesión JWT.
*   **Catálogo Deportivo Expandido (50 productos y 400 variantes)**: Sembrado automático con 50 prendas deportivas y variantes por combinación de talla (S, M, L, XL) y color (Negro, Gris) con control de stock individual.
*   **Búsqueda Básica**: Motor de búsqueda por texto en tiempo real sobre nombres, marcas y descripciones.
*   **Búsqueda Avanzada**: Filtros interactivos de categoría (Calzado, Tops, Bottoms, Accesorios), marcas, talla y rango de precios.
*   **Vista de Detalles**: Modal animado al hacer clic en la imagen del producto, detallando ficha técnica, y sincronización dinámica de existencias de stock según la talla y color elegidos.
*   **Carrito de Compras**: Acumulación temporal de artículos en local storage, control de cantidades (sin superar el límite de stock de la variante) e importe total calculado al instante.
*   **Simulación de Compra**: Checkout protegido (requiere login). Al confirmar, se crea una orden en la BD y se descuenta el stock de las variantes correspondientes de forma transaccional atómica.
*   **Historial de Compras**: Panel privado del usuario con el listado de pedidos anteriores y desglose de artículos comprados.

---

## 📥 Requisitos Previos

*   [Docker](https://www.docker.com/products/docker-desktop) instalado y en ejecución.
*   [Docker Compose](https://docs.docker.com/compose/install/) (incluido en Docker Desktop).

---

## ⚡ Instrucciones para Ejecutar la Aplicación

Para iniciar todo el entorno con un solo comando en la raíz del proyecto, se ejecuta:

```bash
docker-compose up --build
```

Una vez que los contenedores estén activos:
*   **Sitio Web (Tienda)**: Se accede a [http://localhost](http://localhost) (puerto 80).
*   **Administrador de Django**: Se accede a [http://localhost/admin/](http://localhost/admin/).

### 🔑 Credenciales por Defecto (Superusuario Administrador)
*   **Usuario**: `admin`
*   **Contraseña**: `adminpassword`

---

## 🧪 Ejecución de Pruebas Unitarias (Backend)

Se implementó un conjunto de 7 pruebas unitarias de integración que validan el registro, inicio de sesión con JWT, filtros básicos/avanzados, y la integridad de stock transaccional durante el checkout.

Para ejecutar las pruebas unitarias dentro del contenedor del backend en ejecución:

```bash
docker-compose exec backend python manage.py test api.tests
```

---

## 👥 Estructura del Equipo de Trabajo (Roles TSPi)

*   **Isaac Diaz Pérez** (Team Leader / Suplente: Michael Ciprian)
*   **Juan Cubillos Betancourth** (Development Manager / Suplente: Gustavo Chacón)
*   **Michael Ciprian Flórez** (Planning Manager / Suplente: Isaac Diaz)
*   **Nicolás Clavijo Ibagon** (Quality/Process Manager / Suplente: Juan Cubillos)
*   **Sergio Contreras Rodríguez** (Support Manager / Suplente: Nicolás Clavijo)

---

## 🌐 Despliegue en la Nube (Azure Container Apps)

La aplicación ha sido desplegada en **Azure Container Apps** utilizando la CLI de Azure (`az`), optimizada para operar bajo los límites de la **capacidad gratuita de Azure** (Azure Free Tier):

*   **URL de la Aplicación (Frontend)**: [https://frontend.icyforest-b75998fd.eastus.azurecontainerapps.io](https://frontend.icyforest-b75998fd.eastus.azurecontainerapps.io)
*   **Panel de Administración en la Nube**: [https://frontend.icyforest-b75998fd.eastus.azurecontainerapps.io/admin/](https://frontend.icyforest-b75998fd.eastus.azurecontainerapps.io/admin/)
    *   **Usuario**: `admin`
    *   **Contraseña**: `adminpassword`

### 💡 Optimización de Costos y Nivel Gratuito:
1.  **Asignación de Recursos**: Cada contenedor se ejecuta con el perfil mínimo permitido por Azure: **0.25 vCPU** y **0.5 GiB de memoria**.
2.  **Escalado Activo a Cero (`min-replicas 0`)**: Los contenedores del frontend, backend y base de datos se suspenden automáticamente al no recibir solicitudes activas, lo que reduce el consumo de vCPU-segundos y GiB-segundos a cero durante los tiempos de inactividad.
3.  *Nota de Acceso*: La primera solicitud que se realice después de un período de inactividad puede demorar entre 20 y 40 segundos mientras se realiza el arranque en frío (Cold Start) de los contenedores.

### 🧹 Eliminación de Recursos en Azure:
Para evitar cargos futuros de almacenamiento del registro de imágenes o bases de datos una vez finalizada la revisión académica, se recomienda eliminar todo el grupo de recursos ejecutando el siguiente comando:
```bash
az group delete --name rg-volt-athletics --yes --no-wait
```
