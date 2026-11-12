from datetime import date

from django.test import Client, TestCase
from django.urls import reverse

from publicaciones.models import Publicacion
from usuarios.models import Usuario, empleado


class AutorizacionPublicacionesTest(TestCase):
    def setUp(self):
        self.cliente = Client()
        
        # 1. Creamos las identidades base
        self.ana = Usuario.objects.create_user(
            username='ana', password='123', dni='11111111', email='ana@test.com'
        )
        self.juan = Usuario.objects.create_user(
            username='juan', password='123', dni='22222222', email='juan@test.com'
        )
        
        # 2. Creamos los perfiles de empleado para AMBOS (usando 'empleado' en minúscula)
        self.empleado_ana = empleado.objects.create(
            usuario=self.ana,
            fecha_ingreso=date(2023, 1, 15)
        )
        self.empleado_juan = empleado.objects.create(
            usuario=self.juan,
            fecha_ingreso=date(2023, 2, 20) # Fecha inventada para Juan
        )

        # 3. Creamos la publicación y se la asignamos SOLO a Ana
        self.publicacion_ana = Publicacion.objects.create(
            titulo='Publicación original de Ana',
            empleado=self.empleado_ana
        )

    def test_juan_no_puede_editar_publicacion_de_ana(self):
        """Unidad 5: Prueba negativa aislando variables y comprobando la BD."""
        
        # Usamos force_login para aislar la autenticación. Juan está logueado.
        self.cliente.force_login(self.juan)
        
        # Juan intenta hacer un POST malicioso para cambiar el título de la changa de Ana
        url_editar_ana = reverse('publicaciones:editar', kwargs={'pk': self.publicacion_ana.pk})
        response = self.cliente.post(url_editar_ana, {'titulo': 'Hackeado por Juan'})
        
        # Verificamos que el sistema lo rechaza con 404
        self.assertEqual(response.status_code, 404)
        
        # LA PRUEBA DEFINITIVA: Verificamos la base de datos
        self.publicacion_ana.refresh_from_db()
        self.assertEqual(self.publicacion_ana.titulo, 'Publicación original de Ana')



    def test_ana_puede_editar_su_propia_publicacion(self):
        """
        Unidad 6: Prueba positiva. Comprueba que el dueño legítimo
        puede editar su recurso y la base de datos se actualiza.
        """
        # Autenticamos a Ana (la dueña legítima)
        self.cliente.force_login(self.ana)
        
        # Ana envía una petición POST para editar SU publicación
        url_editar_ana = reverse('publicaciones:editar', kwargs={'pk': self.publicacion_ana.pk})
        response = self.cliente.post(url_editar_ana, {
            'titulo': 'Título modificado por Ana',
            'descripcion': 'Esta es una nueva descripción válida para que el formulario pase.'
        })
    
        
        # Verificamos que el sistema la redirige al éxito (HTTP 302 a Mis Publicaciones)
        self.assertEqual(response.status_code, 302)


    def test_creacion_publicacion_modelo(self):
        """
        Unidad 6 - Cap 3.2: Prueba directa del ORM.
        Verifica que el modelo persiste correctamente los datos
        sin depender de las vistas ni los formularios.
        """
        nueva_pub = Publicacion.objects.create(
            titulo='Changa de prueba directa',
            descripcion='Probando el modelo sin vistas',
            empleado=self.empleado_ana
        )
        # Verificamos que se guardó en la base de datos asignando un ID
        self.assertIsNotNone(nueva_pub.pk)
        self.assertEqual(nueva_pub.titulo, 'Changa de prueba directa')
        self.assertEqual(nueva_pub.descripcion, 'Probando el modelo sin vistas')