# MDE LLM SQL Generator

Este es un proyecto base que integra un backend en **Flask** con un frontend en **Svelte**. Usa `rollup` para compilar los assets y un entorno virtual de Python para aislar las dependencias del backend.

---

## 📦 Requisitos previos

- [Python 3.8+](https://www.python.org/)
- [Node.js y npm](https://nodejs.org/)
- [Git](https://git-scm.com/)

---

## 🐍 Crear entorno virtual (backend)

### En Windows:

    > python -m venv venv
    > venv\Scripts\activate.bat
    > pip install -r requirements.txt

### En Linux:

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

### .env

    # .env
    #### DBMATE
    DATABASE_URL=mysql://root:123@localhost:3306/classroom
    #### DATABASE
    DB_HOST=localhost
    DB_PORT=3306
    DB_NAME=classroom
    DB_USER=root
    DB_PASSWORD=123
    #### SERVER
    BASE_URL=http://localhost:5000
    STATIC_URL=http://localhost:5000
    USERNAME=admin
    PASSWORD=123
    #### ACCESS SERVICE
    SYSTEM_ID=1
    X_AUTH_ACCESS_SERVICE=dXNlci1zdGlja3lfc2VjcmV0XzEyMzQ1Njc
    URL_ACCESS_SERVICE=http://localhost:8085
    #### FILES SERVICE
    URL_FILES_SERVICE=http://localhost:4000
    X_AUTH_FILES_SERVICE=dXNlci1zdGlja3lfc2VjcmV0XzEyMzQ1Njc
    #### GOOGLE OAUTH
    GOOGLE_CLIENT_ID=your_google_client_id
    GOOGLE_CLIENT_SECRET=your_google_client_secret
    # PATHS
    ACCESS_PATH=/home/pepe/Documentos/node/access
    FILES_PATH=/home/pepe/Documentos/node/files

Ejemplos de código en Sqlite3

```sql
-- Crear una entidad fuerte
CREATE TABLE paises (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  nombre VARCHAR(40) NOT NULL,
  bandera_url VARCHAR(100) NOT NULL,
  gentilicio VARCHAR(30) NOT NULL
);
-- Crear una entidad debil
CREATE TABLE recurso_coleccion (
  id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  coleccion_id INTEGER NOT NULL,
  recurso_id INTEGER NOT NULL,
  FOREIGN KEY (coleccion_id) REFERENCES coleccion (id),
  FOREIGN KEY (recurso_id) REFERENCES recurso (id)
);
```

### Migraciones con DBMATE

Instalar dependencias:

    $ npm install

Crear migración:

    $ npm run db:new <nombre-migración>

Ejecutar

    $ npm run db:up

Deshacer

    $ npm run db:rollback