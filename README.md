# Veterinaria Córdoba

Proyecto Django: sitio web para la veterinaria "Veterinaria Córdoba" (frontend + backend).

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
