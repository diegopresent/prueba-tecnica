# Proyecto FastAPI y Vue.js

Este proyecto consiste en un backend desarrollado con FastAPI y un frontend desarrollado con Vue.js.

## Repositorio

[https://github.com/diegopresent/prueba-tecnica.git](https://github.com/diegopresent/prueba-tecnica.git)

## Requisitos

Asegúrate de tener instalados los siguientes programas:

- Python 3.7+
- Node.js 14+
- npm o yarn
- MySQL

## Configuración del Backend (FastAPI)

1.  **Clonar el repositorio:**

    ```bash
    git clone [https://github.com/diegopresent/prueba-tecnica.git](https://github.com/diegopresent/prueba-tecnica.git)
    cd prueba-tecnica/backend
    ```

2.  **Crear un entorno virtual (opcional pero recomendado):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Linux/macOS
    venv\Scripts\activate  # En Windows
    ```

3.  **Instalar las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la base de datos:**

    * Asegúrate de que MySQL esté instalado y en ejecución.
    * Crea una base de datos llamada `tienda_db`.
    * Configura las variables de entorno en un archivo `.env` en el directorio `backend`:

        ```
        DATABASE_URL=mysql+aiomysql://root:root@localhost:3306/tienda_db
        USER_DB=root
        PASSWORD_DB=root
        HOST_DB=localhost
        PORT_DB=3306
        DATABASE_NAME=tienda_db
        ```

5.  **Ejecutar las migraciones (si las hay):**

    ```bash
    # Ejemplo con Alembic (si lo usas)
    alembic upgrade head
    ```

6.  **Ejecutar el backend:**

    ```bash
    uvicorn main:app --reload
    ```

    El backend estará disponible en `http://127.0.0.1:8000`.

7.  **Acceder a la documentación Swagger UI:**

    Abre tu navegador y ve a `http://127.0.0.1:8000/docs` para ver la documentación de la API.

## Configuración del Frontend (Vue.js)

1.  **Navegar al directorio del frontend:**

    ```bash
    cd ../frontend
    ```

2.  **Instalar las dependencias:**

    ```bash
    npm install  # o yarn install
    ```

3.  **Ejecutar el frontend:**

    ```bash
    npm run dev  # o yarn dev
    ```

    El frontend estará disponible en `http://localhost:5173`.

## Variables de Entorno

El backend requiere un archivo `.env` en el directorio `backend` con las siguientes variables:

DATABASE_URL=mysql+aiomysql://root:root@localhost:3306/tienda_db
USER_DB=root
PASSWORD_DB=root
HOST_DB=localhost
PORT_DB=3306
DATABASE_NAME=tienda_db
