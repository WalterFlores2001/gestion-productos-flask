# 🛒 Gestión de Productos de Supermercado

![Licencia](https://img.shields.io/badge/Licencia-MIT-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12%2B-blue)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-brightgreen)
![Tailwind CSS](c)

Una aplicación web robusta para la gestión de productos de supermercado, desarrollada con una moderna arquitectura de microservicios que combina la potencia del backend en **Flask** (Python) con un frontend con **Bootstrap**, pero con una proxima implementación de reactivo en **Vue.js**, enriquecido con **Tailwind CSS** y optimizado con **Vite**.

## 📋 Tabla de Contenidos

- [Resumen](#-resumen)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Guía de Instalación](#-guía-de-instalación)
  - [1. Configuración del Entorno](#1-configuración-del-entorno)
  - [2. Variables de Entorno](#2-variables-de-entorno)
  - [3. Base de Datos y Migraciones](#3-base-de-datos-y-migraciones)
- [Ejecución del Proyecto](#-ejecución-del-proyecto)
- [Gestión de Usuarios](#-gestión-de-usuarios)
- [Sistema de Correos Electrónicos](#-sistema-de-correos-electrónicos)
- [Resolución de Problemas](#-resolución-de-problemas)
- [Contribuciones](#-contribuciones)

## 📝 Resumen

Esta aplicación permite gestionar de forma eficiente y segura el inventario de productos de un supermercado, con funcionalidades como:

- ✅ **Gestión completa de productos** (CRUD)
- ✅ **Autenticación de usuarios** con diferentes niveles de acceso
- ✅ **Verificación por email** para nuevos registros
- ✅ **Interfaz responsiva y moderna** optimizada para distintos dispositivos
- ✅ **Dashboard analítico** para visualización de datos

## 🚀 Tecnologías

### Backend:
- **Flask**: Framework web ligero y versátil para Python
- **PostgreSQL**: Sistema de gestión de bases de datos relacional
- **SQLAlchemy**: ORM para interacción con la base de datos
- **Flask-Login**: Gestión de sesiones de usuario
- **Flask-Mail**: Envío de correos electrónicos
- **Alembic**: Control de migraciones de base de datos

### Frontend:
- **Bootstrap**: Framework multiplataforma o conjunto de herramientas de código abierto para diseño de sitios y aplicaciones web
- **Vue.js 3**: Framework progresivo para construir interfaces de usuario
- **Vite**: Herramienta de construcción optimizada para desarrollo frontend
- **Tailwind CSS**: Framework CSS utilitario para diseño rápido y responsivo
- **Axios**: Cliente HTTP para comunicación con el backend

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python** (3.8 o superior)
- **PostgreSQL** (versión 12 o superior recomendada)
- **Node.js** y **npm** (versiones LTS recomendadas)
- **Git**


## 🔧 Guía de Instalación

### 1. Configuración del Entorno

**Paso 1**: Clonar el repositorio y navegar al directorio del proyecto
```bash
git clone https://github.com/WalterFlores2001/gestion-productos-flask.git
cd gestion-productos-flask
```

**Paso 2**: Crear y activar un entorno virtual

```bash
# En Windows
python -m venv .venv
.venv\Scripts\activate

# En macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

**Paso 3**: Instalar las dependencias de Python
```bash
pip install -r requirements.txt
```

### 2. Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con la siguiente información:

```
# Configuración general
SECRET_KEY=tu_clave_secreta_muy_larga_y_compleja
FLASK_ENV=development
FLASK_DEBUG=True

# Configuración de la base de datos
DATABASE_URL=postgresql://usuario:contraseña@localhost/supermarket

# Configuración de correo electrónico
EMAIL_USER=tu_correo@gmail.com
EMAIL_PASS=tu_contraseña_de_app_gmail
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
```

### 3. Base de Datos y Migraciones

**Paso 1**: Asegúrate de tener PostgreSQL en ejecución y crea una base de datos llamada "supermarket"

```bash
# Usando psql
psql -U postgres
CREATE DATABASE supermarket;
\q
```

**Paso 2**: Inicializa el directorio de migraciones (solo la primera vez)
```bash
flask db init
```

**Paso 3**: Crea y aplica las migraciones
```bash
flask db migrate -m "Inicialización de modelos"
flask db upgrade
```

### 4. Instalación del Frontend

**Paso 1**: Navegar al directorio frontend e instalar dependencias
```bash
cd frontend
npm install
```

**Paso 2**: Configurar Tailwind CSS
```bash
# Instalación estándar
npx tailwindcss init -p

# Si prefieres Tailwind CSS v3 (más estable)
npm install tailwindcss@3 postcss autoprefixer -D
npx tailwindcss init -p
```

## 🚀 Ejecución del Proyecto

### Backend (Flask)

```bash
# Desde la raíz del proyecto, con el entorno virtual activo
flask run
```
La API estará disponible en: http://127.0.0.1:5000/

## 👥 Gestión de Usuarios

El sistema cuenta con un sistema de autenticación que requiere verificación por correo electrónico. Si necesitas verificar manualmente un usuario (para pruebas):

```sql
-- Ejecuta esto en tu cliente SQL o pgAdmin
UPDATE public.user
SET is_verified = true
WHERE email = 'usuario@ejemplo.com';
```

## 📧 Sistema de Correos Electrónicos

La aplicación utiliza Flask-Mail para enviar:
- Correos de verificación de cuenta
- Restablecimiento de contraseña
- Notificaciones del sistema

> **Nota**: Para usar Gmail como servidor SMTP, debes generar una "contraseña de aplicación" específica en la configuración de seguridad de tu cuenta Google.

## 🔍 Resolución de Problemas

### Problemas con Tailwind CSS

Si experimentas problemas con la versión más reciente de Tailwind, puedes utilizar la versión 3:

```bash
# Eliminar la instalación actual
rmdir /s /q node_modules
del package-lock.json

# Reinstalar con versión específica
npm init -y
npm install tailwindcss@3 postcss autoprefixer -D
npx tailwindcss init -p
```

### Errores de migración

Si encuentras errores durante las migraciones:

```bash
# Eliminar la migración problemática
flask db stamp head
flask db migrate -m "Reinicio de migraciones"
flask db upgrade
```

## 👨‍💻 Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Haz fork del repositorio
2. Crea una rama para tu función (`git checkout -b feature/amazing-feature`)
3. Haz commit de tus cambios (`git commit -m 'Añade una función increíble'`)
4. Realiza push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request


📘 **Documentación adicional**: Para información más detallada, consulta el manual en PDF incluido.
