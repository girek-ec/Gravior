from django.test import TestCase
from django.urls import reverse

PAGES = [
    ('inicio:index', '/'),
    ('empresa:index', '/nosotros/'),
    ('genetica:index', '/genetica/'),
    ('calidad:index', '/calidad-bioseguridad/'),
    ('productos:index', '/productos/'),
    ('infraestructura:index', '/instalaciones/'),
    ('equipo:index', '/equipo/'),
    ('aliados:index', '/aliados/'),
    ('actualidad:index', '/actualidad/'),
    ('contacto:index', '/contacto/'),
]

PENDING_DETAILS = ['genetica:detail', 'productos:detail', 'infraestructura:detail']


class PublicPagesTests(TestCase):
    def test_pages_resolve_and_render(self):
        for name, path in PAGES:
            with self.subTest(name=name):
                self.assertEqual(reverse(name), path)
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'base.html')

    def test_pending_detail_routes_return_404(self):
        for name in PENDING_DETAILS:
            with self.subTest(name=name):
                response = self.client.get(reverse(name, kwargs={'slug': 'ejemplo'}))
                self.assertEqual(response.status_code, 404)

    def test_post_detail_mockup_renders(self):
        response = self.client.get(reverse('actualidad:detail', kwargs={'slug': 'ejemplo'}))
        self.assertEqual(response.status_code, 200)

    def test_admin_login_loads(self):
        response = self.client.get(reverse('admin:login'))
        self.assertEqual(response.status_code, 200)
