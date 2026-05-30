# Veterinaria Petit

Proyecto Django: sitio web para la veterinaria "Petit" (frontend + backend).

## Descripción

Aplicación web creada con Django que incluye: autenticación, blog, tienda, turnos, y gestión de mascotas y veterinarios.

Repositorio en GitHub: https://github.com/santifigu/veterinaria_petit

## Requisitos

- Python 3.10 o superior
- pip

## Instalación rápida (Windows PowerShell)

```powershell
python -m venv env_petit
& env_petit\Scripts\Activate.ps1
pip install -r requirements.txt  # si existe
# Si no hay requirements.txt, instalar Django y dependencias necesarias
# pip install django

# Configurar variables de entorno (SECRET_KEY, DEBUG, DB) según tu entorno

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Notas

- La rama `main` ya fue empujada a GitHub.
- Se creó una rama de respaldo `backup-before-email-change` localmente antes de reescribir los commits para ajustar el email público.

Si querés que agregue un `.gitignore` para Django o un `requirements.txt`, decime y lo agrego y commiteo también.
