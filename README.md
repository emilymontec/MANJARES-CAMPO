# MANJARES DEL CAMPO

Plataforma de e-commerce fullstack para la venta de productos agrícolas y artesanales del campo. Conecta productores locales con compradores finales, gestionando el ciclo completo de compra: catálogo, carrito, pagos, envíos y notificaciones por WhatsApp.

---

## Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.12 + Django |
| Base de Datos | PostgreSQL |
| Frontend | HTML5 + CSS3 + JavaScript |
| Notificaciones | Plugin WhatsApp |

---

## Funcionalidades

- **Catálogo de productos** con filtros por categoría
- **Carrito de compras** con gestión de cantidades
- **Confirmación de pagos** manual por el administrador
- **Gestión de pedidos** con seguimiento de estados
- **Rastreo de envíos** en tiempo real
- **Notificaciones automáticas por WhatsApp** en cada actualización del pedido
- **Panel de administración** para gestionar productos, pedidos y envíos

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/emilymontec/MANJARES-CAMPO.git
cd MANJARES-CAMPO

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env  # Editar con tus credenciales

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Correr el servidor
python manage.py runserver
```

---

## ⚙️ Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgres://usuario:password@localhost:5432/manjarescampo_db
WHATSAPP_NUMBER=numero_whatsapp
DEFAULT_SHIPPING_COST=10000
FREE_SHIPPING_OVER=100000
DISCOUNT_PERCENT=0
BUSINESS_HOURS=horarios_habiles
SOCIAL_FACEBOOK_URL=tu_pagina_facebook
SOCIAL_INSTAGRAM_URL=tu_perfil_instagram
```

---

## Estructura del Proyecto

```
MANJARES-CAMPO/
├── manjares/        # Configuración principal
├── catalogo/        # App: catálogo de productos
├── carrito/         # App: carrito de compras
├── pedidos/         # App: gestión de pedidos
├── envios/          # App: rastreo de envíos
├── whatsapp/        # App: integración WhatsApp
└── static/          # Archivos estáticos
```

---

## URLs Principales

| URL | Descripción |
|-----|-------------|
| `/` | Página principal / catálogo |
| `/carrito/` | Carrito de compras |
| `Directamente a Whatsapp` | Crear nuevo pedido |
| `/rastreo/` | Rastrear envío |
| `/dashboard/admin/` | Panel de administración |

---

## Para información más detallada

Consulte la documentación: [Documentación (descargar pdf)](https://github.com/emilymontec/MANJARES-CAMPO/raw/main/documentation.pdf)