from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

Usuario = get_user_model()

class SeguridadAccesosTest(TestCase):
    def setUp(self):
        # Preparamos un cliente (navegador simulado)
        self.cliente = Client()
        # Creamos un usuario de prueba
        self.usuario_juan = Usuario.objects.create_user(
            username='juan_prueba', 
            password='Password123'
        )

    def test_anonimo_es_redirigido_al_login(self):
        """Unidad 5: Validar que el LoginRequiredMixin expulsa al anónimo."""
        # Intentamos entrar a crear publicación sin estar logueados
        response = self.cliente.get(reverse('publicaciones:crear')) 
        
        # El sistema debe responder 302 (Redirección)
        self.assertEqual(response.status_code, 302)

        print("LA URL DE REDIRECCIÓN ES:", response.url)
        # Y debe mandarnos a la URL que configuramos en settings.LOGIN_URL
        self.assertTrue(response.url.startswith('/usuarios/login/'))