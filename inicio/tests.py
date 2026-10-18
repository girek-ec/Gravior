from django.test import TestCase

from .models import Differential, ProcessStep, Statistic


class HomeSectionsTests(TestCase):
    def test_empty_sections_are_omitted(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        for marker in ('gym-and-fitness-slider', 'pricing-table-style-09', 'counter-style-07', 'process-step-style-10'):
            self.assertNotContains(response, marker)

    def test_sections_render_admin_content(self):
        Differential.objects.create(title='Diferencial X', description='Texto X', order=1)
        Differential.objects.create(title='Solo Nosotros', description='Texto', show_home=False, order=2)
        ProcessStep.objects.create(number='07', title='Etapa X', description='Detalle', order=1)
        Statistic.objects.create(title='Indicador X', value=12, suffix='%', order=1)
        Statistic.objects.create(title='Inactivo', value=3, is_active=False, order=2)
        response = self.client.get('/')
        self.assertContains(response, 'Diferencial X')
        self.assertNotContains(response, 'Solo Nosotros')
        self.assertContains(response, 'Etapa X')
        self.assertContains(response, 'data-to="12"')
        self.assertNotContains(response, 'Inactivo')
        about = self.client.get('/nosotros/')
        self.assertContains(about, 'Solo Nosotros')
        self.assertContains(about, 'counter-style-07')
