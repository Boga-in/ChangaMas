from django.db import migrations


def crear_rol_visores(apps, schema_editor):
    #instancia a partir de modelos historicos segun dependencia
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Publicacion = apps.get_model('publicaciones', 'Publicacion')

    # Obtiene o Crear el grupo "visores" y le asigna el permiso "puede_reportar"
    grupo_visores, creado = Group.objects.get_or_create(name='visores')
    content_type = ContentType.objects.get_for_model(Publicacion)
    #instancia del permiso "puede_reportar" usando el content_type de Publicacion
    #ACLARACION: antes de poder asigar el permiso al grupo, debemos asegurarnos de que el permiso "puede_reportar" exista en la base de datos.
    #para ello, debemos haber ejecutado previamente las migraciones que crean el modelo Publicacion y su permiso asociado. Si el permiso no existe, este código lanzará un error.
    #vease 0008_alter_publicacion_options.py
    permiso_reportar = Permission.objects.get(
        codename='puede_reportar',
        content_type=content_type,
    )

    #se asigna el permiso al grupo "visores"
    grupo_visores.permissions.add(permiso_reportar)

class Migration(migrations.Migration):
    # Define la dependencia de la migración anterior
    dependencies = [
        ('publicaciones', '0008_alter_publicacion_options'),
    ]
    # indicamo que funcion ejecutar en esta migracion para crear el grupo y asignarle el permiso
    operations = [
        migrations.RunPython(crear_rol_visores),
    ]