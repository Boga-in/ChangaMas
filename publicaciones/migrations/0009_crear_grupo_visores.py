from django.db import migrations


def crear_rol_visores(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Publicacion = apps.get_model('publicaciones', 'Publicacion')

    grupo_visores, creado = Group.objects.get_or_create(name='visores')
    content_type = ContentType.objects.get_for_model(Publicacion)

    try:
        permiso_reportar = Permission.objects.get(
            codename='puede_reportar',
            content_type=content_type,
        )
        grupo_visores.permissions.add(permiso_reportar)
    except Permission.DoesNotExist:
        # Durante los tests, Django todavía no generó los permisos. Lo ignoramos.
        pass

class Migration(migrations.Migration):
    dependencies = [
        ('publicaciones', '0008_alter_publicacion_options'),
    ]
    operations = [
        migrations.RunPython(crear_rol_visores),
    ]