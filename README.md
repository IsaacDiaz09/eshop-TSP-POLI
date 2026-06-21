# Volt Athletics - E-commerce Deportivo

Volt Athletics es una aplicación e-commerce de indumentaria deportiva desarrollada bajo la metodología **TSPi/PSP**. La solución frontend + backend se ejecuta localmente mediante **un único comando de Docker**.

---

## 🛠️ Arquitectura y Tecnologías

El sistema consta de tres contenedores coordinados:
*   **Frontend (Nginx - Puerto 80)**: Sirve la SPA estática (HTML5, Vanilla JS, Bootstrap 5) y actúa como proxy inverso hacia la API y panel administrativo.
*   **Backend (Django - Puerto 80)**: API REST (Django REST Framework) con autenticación JWT y paginación de 9 productos.
*   **Base de Datos (PostgreSQL - Puerto 5432)**: Persistencia de datos mediante el volumen `postgres_data`.

---

## 🚀 Módulos Funcionales

*   **Autenticación**: Registro e inicio de sesión seguros mediante tokens JWT.
*   **Catálogo Expandido**: 50 artículos deportivos con 400 variantes (tallas S/M/L/XL, colores Negro/Gris) y stock dinámico.
*   **Buscador y Filtros**: Búsqueda por texto y filtros avanzados (categoría, marca, talla, precio).
*   **Detalles y Carrito**: Modal con existencias en tiempo real y persistencia local del carrito.
*   **Compra y Pedidos**: Checkout transaccional atómico que descuenta stock, e historial de pedidos por usuario.

---

## ⚡ Ejecución Local

### Requisitos
*   [Docker](https://www.docker.com/products/docker-desktop) y [Docker Compose](https://docs.docker.com/compose/install/) instalados.

### Comandos de Ejecución y Pruebas
```bash
# Iniciar la aplicación
docker-compose up --build

# Ejecutar pruebas unitarias (7 pruebas de integración)
docker-compose exec backend python manage.py test api.tests
```

### Accesos Locales
*   **Tienda (Frontend)**: [http://localhost](http://localhost) (Puerto 80)
*   **Administrador de Django**: [http://localhost/admin/](http://localhost/admin/) (admin / adminpassword)

---

## 🌐 Despliegue en la Nube (Azure Container Apps)

La solución está desplegada en **Azure Container Apps** configurada bajo el nivel gratuito (Free Tier):

*   **Sitio Web**: [https://frontend.icyforest-b75998fd.eastus.azurecontainerapps.io](https://frontend.icyforest-b75998fd.eastus.azurecontainerapps.io)
*   **Panel de Administración**: [https://frontend.icyforest-b75998fd.eastus.azurecontainerapps.io/admin/](https://frontend.icyforest-b75998fd.eastus.azurecontainerapps.io/admin/) (admin / adminpassword)

> [!NOTE]
> **Arranque en Frío**: Para optimizar costos, se configuraron recursos mínimos (0.25 vCPU, 0.5 GiB) y escalado activo a cero (`min-replicas 0`). Tras inactividad, la primera solicitud puede demorar entre 20 y 40 segundos.

### Comando de Limpieza (Azure)
```bash
az group delete --name rg-volt-athletics --yes --no-wait
```

---

## 👥 Equipo de Trabajo (Roles TSPi)

*   **Isaac Diaz Pérez** (Team Leader / Suplente: Michael Ciprian)
*   **Juan Cubillos Betancourth** (Development Manager / Suplente: Gustavo Chacón)
*   **Michael Ciprian Flórez** (Planning Manager / Suplente: Isaac Diaz)
*   **Nicolás Clavijo Ibagon** (Quality/Process Manager / Suplente: Juan Cubillos)
*   **Sergio Contreras Rodríguez** (Support Manager / Suplente: Nicolás Clavijo)
