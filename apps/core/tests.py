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


class SeedBloqueATests(TestCase):
    def setUp(self):
        import shutil
        import tempfile
        from django.test import override_settings
        self.media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.media, ignore_errors=True)
        override = override_settings(MEDIA_ROOT=self.media)
        override.enable()
        self.addCleanup(override.disable)

    def run_seed(self):
        from io import StringIO
        from django.core.management import call_command
        call_command('seed_bloque_a', stdout=StringIO())

    def test_seed_is_idempotent_and_keeps_edits(self):
        from apps.inicio.models import Differential, HeroSlide, Statistic
        from .models import CallToAction, SiteConfiguration
        self.run_seed()
        self.assertEqual(SiteConfiguration.objects.count(), 1)
        self.assertEqual(HeroSlide.objects.count(), 3)
        self.assertEqual(Differential.objects.count(), 6)
        self.assertEqual(Statistic.objects.count(), 0)

        config = SiteConfiguration.objects.get()
        config.company_name = 'Editado por el cliente'
        config.save()
        slide = HeroSlide.objects.first()
        slide.title = 'Título editado'
        slide.save()
        CallToAction.objects.filter(code='home_process').delete()

        self.run_seed()
        self.assertEqual(SiteConfiguration.objects.get().company_name, 'Editado por el cliente')
        self.assertEqual(HeroSlide.objects.count(), 3)
        self.assertTrue(HeroSlide.objects.filter(title='Título editado').exists())
        self.assertTrue(CallToAction.objects.filter(code='home_process').exists())

    def test_pages_render_with_seeded_data(self):
        self.run_seed()
        for path in ('/', '/nosotros/', '/contacto/'):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)


class BlockAAdminTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        user = get_user_model().objects.create_superuser('admin-test', 'admin@example.com', 'x')
        self.client.force_login(user)

    def test_changelists_load(self):
        for name in ('core_corporateemail', 'core_socialnetwork', 'core_calltoaction',
                     'inicio_heroslide', 'inicio_differential', 'inicio_statistic', 'inicio_processstep'):
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(f'admin:{name}_changelist')).status_code, 200)
                self.assertEqual(self.client.get(reverse(f'admin:{name}_add')).status_code, 200)

    def test_site_configuration_singleton(self):
        from .models import SiteConfiguration
        response = self.client.get(reverse('admin:core_siteconfiguration_changelist'))
        self.assertRedirects(response, reverse('admin:core_siteconfiguration_add'))
        config = SiteConfiguration.objects.create(
            company_name='Empresa', logo='site/logo.png', short_description='Desc',
            whatsapp_number='+593 00 000 0000', copyright_text='Copyright 2026')
        response = self.client.get(reverse('admin:core_siteconfiguration_changelist'))
        self.assertRedirects(response, reverse('admin:core_siteconfiguration_change', args=[config.pk]),
                             fetch_redirect_response=False)
        self.assertEqual(self.client.get(reverse('admin:core_siteconfiguration_add')).status_code, 403)
        self.assertEqual(self.client.get(reverse('admin:core_siteconfiguration_delete', args=[config.pk])).status_code, 403)

    def test_admin_index_groups_order(self):
        response = self.client.get(reverse('admin:index'))
        labels = [app['app_label'] for app in response.context['app_list']]
        self.assertEqual(labels[:2], ['core', 'inicio'])
        inicio = next(app for app in response.context['app_list'] if app['app_label'] == 'inicio')
        self.assertEqual([m['object_name'] for m in inicio['models']],
                         ['HeroSlide', 'Differential', 'Statistic', 'ProcessStep'])
