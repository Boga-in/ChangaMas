========================================================================
PROYECTO CHANGAMAS - GUÍA PARA LEVANTAR EL ENTORNO LOCAL DESDE CERO
========================================================================

Buenas! Acá dejo el paso a paso para clonar, configurar y levantar el
proyecto en una máquina local sin renegar con dependencias ni rutas.

------------------------------------------------------------------------
REQUISITOS PREVIOS
------------------------------------------------------------------------
- Tener instalado Python (3.10 o superior).
- Tener Git configurado en la máquina.
- (Opcional) VS Code con la extensión oficial de Python.

------------------------------------------------------------------------
1. CLONAR EL REPOSITORIO
------------------------------------------------------------------------
Abrimos la terminal en la carpeta donde guardamos los proyectos,
clonamos el repo y nos metemos adentro del directorio:

    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DE_LA_CARPETA>

Nota: Si hay que trabajar sobre una rama específica que no sea main,
traemos las referencias y nos movemos antes de seguir:

    git fetch --all
    git switch <nombre-de-la-rama>

------------------------------------------------------------------------
2. CREAR Y ACTIVAR EL ENTORNO VIRTUAL (.venv)
------------------------------------------------------------------------
Para no ensuciar el Python global del sistema operativo y evitar
conflictos de versiones entre materias/proyectos, armamos un entorno
virtual aislado llamado .venv en la raíz:

En Linux / macOS:
    python3 -m venv .venv
    source .venv/bin/activate

En Windows (PowerShell):
    python -m venv .venv
    .venv\Scripts\Activate.ps1

En Windows (CMD):
    python -m venv .venv
    .venv\Scripts\activate.bat

(Chequear que aparezca el prefijo (.venv) a la izquierda en la consola
antes de tirar los siguientes comandos).

------------------------------------------------------------------------
3. INSTALAR LAS DEPENDENCIAS
------------------------------------------------------------------------
Con el entorno activado, actualizamos pip por las dudas e instalamos
todo lo que figura en el requirements.txt (Django, Pillow, toolbar, etc.):

En Linux / macOS:
    pip install --upgrade pip (python.exe -m pip install --upgrade pip - en windows)
    pip install -r requirements.txt

En Windows:
    python.exe -m pip install --upgrade pip
    pip install -r requirements.txt

------------------------------------------------------------------------
4. VARIABLES DE ENTORNO (SI APLICA)
------------------------------------------------------------------------
Si el proyecto tiene configurado un archivo .env para ocultar la
SECRET_KEY o credenciales, hay que crearlo en la raíz (al mismo nivel
que manage.py) con los valores de desarrollo:

    SECRET_KEY=clave-secreta-para-desarrollo-local
    DEBUG=True

Existe un ejemplo de como debe configurarse esta configuarcion .env.example

------------------------------------------------------------------------
5. PREPARAR LA BASE DE DATOS (MIGRACIONES)
------------------------------------------------------------------------
Como db.sqlite3 está ignorado en el .gitignore, cada uno genera su
propia instancia local. Corremos las migraciones para armar las tablas
(incluyendo nuestro modelo de usuario personalizado y publicaciones):

    python manage.py migrate

Nota: Si por algún motivo faltan archivos dentro de las carpetas
migrations/ de las apps, tirar primero:

    python manage.py makemigrations
    python manage.py migrate

------------------------------------------------------------------------
6. CREAR UN SUPERUSUARIO
------------------------------------------------------------------------
Como varias vistas tienen LoginRequiredMixin y validaciones de permisos,
necesitamos un usuario registrado para testear el CRUD completo:

    python manage.py createsuperuser

La consola va a pedir username, email (puede quedar vacío) y password.

------------------------------------------------------------------------
7. LEVANTAR EL SERVIDOR DE DESARROLLO
------------------------------------------------------------------------
Arrancamos el servidor local de Django:

    python manage.py runserver

Si no arrojo ningún error, ya podemos entrar desde el navegador:
- App principal: http://127.0.0.1:8000/
- Panel Admin:   http://127.0.0.1:8000/admin/

------------------------------------------------------------------------
NOTAS ADICIONALES / TROUBLESHOOTING RÁPIDO
------------------------------------------------------------------------
- Imágenes (Media): La carpeta media/ no se sube al repo. Django la va
  a crear automáticamente en la raíz apenas suban la primera foto desde
  el formulario de crear publicación.
- Estilos (Static): Los CSS están centralizados en static/css/. Si no
  se ven los cambios al editar estilos, probar recargar el navegador
  forzando limpieza de caché (Ctrl + Shift + R).
- Al volver a abrir el proyecto otro día: acordarse siempre de volver
  a activar el entorno virtual (.venv) antes de tirar el runserver.
========================================================================