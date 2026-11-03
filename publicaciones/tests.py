from django.test import TestCase, Client
from django.urls import reverse
from usuarios.models import Usuario, empleado 
from publicaciones.models import Publicacion
from datetime import date

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