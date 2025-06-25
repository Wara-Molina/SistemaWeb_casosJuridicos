#  Sistema Web para Atención y Seguimiento de Casos Jurídicos

Este sistema web está diseñado para gestionar y hacer seguimiento de casos jurídicos en despachos legales. Permite registrar clientes, abogados, casos, pagos en cuotas, generar recibos, gestionar documentos y controlar el estado de los procesos judiciales.

# Usuarios y contraseñas

- Administrador
  brayan  contraseña:123

- Secretaria
  secretaria   contraseña: 123

##  Funcionalidades principales

- Gestión de usuarios con roles: abogado, secretaria, administrador.
- Registro y edición de clientes.
- Creación y seguimiento de casos jurídicos.
- Registro de pagos por cuotas asociados a un caso.
- Validación automática del total pagado vs. monto del caso.
- Generación de recibos por cada cuota pagada.
- Administración de estados de pago y estados de usuario.
- Vistas separadas (`views/`) para control limpio y organizado.
- Panel de administración con CRUD completo.

##  Tecnologías utilizadas

- **Backend:** Python, Flask
- **Base de datos:** SQLite (o PostgreSQL/MySQL opcional)
- **ORM:** SQLAlchemy
- **Frontend:** HTML5, Bootstrap 5, Jinja2
- **Otros:** Werkzeug, Flask Blueprints

##  Estructura de carpetas

sistema_juridico/
│
├── controllers/ # Controladores Flask
│ ├── usuario_controller.py
│ ├── cliente_controller.py
│ ├── pago_controller.py
│ └── ...
│
├── models/ # Modelos SQLAlchemy
│ ├── usuario_model.py
│ ├── cliente_model.py
│ ├── caso_model.py
│ ├── pago_model.py
│ └── ...
│
├── views/ # Funciones de renderizado
│ ├── usuario_view.py
│ ├── pago_view.py
│ └── ...
│
├── templates/ # Vistas HTML con Jinja2
│ ├── pagos/
│ ├── usuarios/
│ ├── base.html
│ └── ...
│
├── database.py # Configuración de SQLAlchemy
├── run.py # Punto de entrada principal
└── requirements.txt # Dependencias