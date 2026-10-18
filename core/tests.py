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


class SiteContextProcessorTests(TestCase):
    def _config(self, **kwargs):
        from .models import SiteConfiguration
        data = dict(company_name='Empresa', logo='site/logo.png', short_description='Desc',
                    whatsapp_number='+593 00 000 0000', copyright_text='Copyright 2026')
        data.update(kwargs)
        return SiteConfiguration.objects.create(**data)

    def test_without_configuration(self):
        response = self.client.get('/')
        self.assertIsNone(response.context['site_config'])
        self.assertEqual(response.context['whatsapp_url'], '')
        self.assertEqual(response.context['corporate_emails'], [])
        self.assertEqual(response.context['social_networks'], [])

    def test_whatsapp_url(self):
        config = self._config(whatsapp_message='Hola, quiero información')
        self.assertEqual(config.whatsapp_url, 'https://wa.me/593000000000?text=Hola%2C%20quiero%20informaci%C3%B3n')
        response = self.client.get('/')
        self.assertEqual(response.context['whatsapp_url'], config.whatsapp_url)

    def test_whatsapp_disabled(self):
        self._config(whatsapp_enabled=False)
        self.assertEqual(self.client.get('/').context['whatsapp_url'], '')

    def test_only_active_items(self):
        from .models import CorporateEmail, SocialNetwork
        CorporateEmail.objects.create(label='Info', email='info@example.com')
        CorporateEmail.objects.create(label='Oculto', email='x@example.com', is_active=False)
        SocialNetwork.objects.create(name='Red', url='https://example.com', is_active=False)
        context = self.client.get('/').context
        self.assertEqual([e.label for e in context['corporate_emails']], ['Info'])
        self.assertEqual(context['social_networks'], [])

    def test_singleton_rejects_second_instance(self):
        from django.core.exceptions import ValidationError
        from .models import SiteConfiguration
        self._config()
        with self.assertRaises(ValidationError):
            SiteConfiguration(company_name='Otra').full_clean()
