from django.test import TestCase
from .models import Ambulancia
from django.utils import timezone

class AmbulanciaModelTest(TestCase):

    def setUp(self):
        # Crear una ambulancia de prueba
        self.ambulancia = Ambulancia.objects.create(
            movil='AMB-001',
            clasevehiculo='Camioneta',
            marca='Toyota',
            modelo=2020,
            placa='ABC123',
            ven_soat=timezone.now().date(),
            ven_tecno=timezone.now().date(),
            frontal='path/to/image.jpg',
            lateral='path/to/image2.jpg'
        )

    def test_creacion_ambulancia(self):
        """Verifica que la ambulancia se cree correctamente"""
        self.assertEqual(self.ambulancia.movil, 'AMB-001')
        self.assertEqual(self.ambulancia.marca, 'Toyota')
        self.assertTrue(isinstance(self.ambulancia, Ambulancia))

    def test_str_method(self):
        """Verifica que el método __str__ devuelve el nombre del móvil"""
        self.assertEqual(str(self.ambulancia), 'AMB-001')

    def test_campos_obligatorios(self):
        """Verifica que los campos obligatorios no estén vacíos"""
        self.assertIsNotNone(self.ambulancia.modelo)
        self.assertIsNotNone(self.ambulancia.placa)