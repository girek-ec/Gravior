from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from apps.aliados.models import Partner
from apps.equipo.models import TeamMember

from .models import CallToAction
from .tests_bloque_b import TempMediaMixin


class SeedDMixin(TempMediaMixin):
    def seed_d(self, *args):
        out = StringIO()
        call_command('seed_bloque_d', *args, stdout=out)
        return out.getvalue()


class SeedBloqueDTests(SeedDMixin, TestCase):
    def test_seed_loads_generic_records(self):
        output = self.seed_d()
        self.assertEqual(TeamMember.objects.count(), 6)
        self.assertEqual(Partner.objects.count(), 7)
        self.assertTrue(CallToAction.objects.filter(code='team_contact').exists())
        self.assertTrue(all(m.name.startswith('Nombre del integrante') for m in TeamMember.objects.all()))
        self.assertTrue(all(m.position == 'Cargo del integrante' for m in TeamMember.objects.all()))
        self.assertTrue(all(p.name.startswith('Aliado de ejemplo') for p in Partner.objects.all()))
        self.assertFalse(Partner.objects.filter(name__icontains='cobb').exists())
        self.assertIn('Cobb', output)

    def test_personal_data_stays_empty(self):
        self.seed_d('--fill-blanks')
        for member in TeamMember.objects.all():
            self.assertEqual((member.email, member.phone, member.linkedin_url), ('', '', ''))
            for field in ('specialty', 'short_bio', 'biography'):
                self.assertTrue(getattr(member, field), field)

    def test_placeholder_logo_is_a_valid_png(self):
        self.seed_d()
        partner = Partner.objects.first()
        self.assertTrue(partner.logo.name.endswith('.png'))
        with Image.open(partner.logo.path) as logo:
            self.assertEqual(logo.size, (300, 120))

    def test_idempotent_and_fill_blanks(self):
        self.seed_d()
        TeamMember.objects.filter(order=1).update(specialty='', name='Nombre del integrante 1')
        TeamMember.objects.filter(order=2).update(short_bio='Resumen del cliente')
        Partner.objects.filter(order=1).update(description='')
        self.seed_d()
        self.assertEqual(TeamMember.objects.count(), 6)
        self.assertEqual(TeamMember.objects.get(order=1).specialty, '')
        output = self.seed_d('--fill-blanks')
        self.assertTrue(TeamMember.objects.get(order=1).specialty)
        self.assertEqual(TeamMember.objects.get(order=2).short_bio, 'Resumen del cliente')
        self.assertTrue(Partner.objects.get(order=1).description)
        self.assertIn('specialty', output)
        self.assertIn('No había campos vacíos', self.seed_d('--fill-blanks'))


class BlockDAdminTests(SeedDMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(get_user_model().objects.create_superuser('admin-d', 'd@example.com', 'x'))

    def test_changelists_and_forms(self):
        self.seed_d()
        for name in ('equipo_teammember', 'aliados_partner'):
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(f'admin:{name}_changelist')).status_code, 200)
                self.assertEqual(self.client.get(reverse(f'admin:{name}_add')).status_code, 200)
        member = TeamMember.objects.first()
        response = self.client.get(reverse('admin:equipo_teammember_change', args=[member.pk]))
        self.assertContains(response, member.photo.url)
        partner = Partner.objects.first()
        response = self.client.get(reverse('admin:aliados_partner_change', args=[partner.pk]))
        self.assertContains(response, partner.logo.url)

    def test_admin_groups_order(self):
        labels = [app['app_label'] for app in self.client.get(reverse('admin:index')).context['app_list']]
        self.assertEqual(labels[:9], ['core', 'inicio', 'empresa', 'genetica', 'calidad', 'productos',
                                      'infraestructura', 'equipo', 'aliados'])


class BlockDViewsTests(SeedDMixin, TestCase):
    def test_pages_with_empty_tables(self):
        for path in ('/equipo/', '/aliados/', '/'):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)
        self.assertNotContains(self.client.get('/equipo/'), 'team-style-08')
        aliados = self.client.get('/aliados/')
        self.assertNotContains(aliados, 'client-box')
        self.assertNotContains(aliados, 'review-style-04"')
        self.assertNotContains(self.client.get('/'), 'id="tab_nine1"')

    def test_team_page(self):
        self.seed_d()
        response = self.client.get('/equipo/')
        self.assertContains(response, 'Nombre del integrante 1', count=1)
        self.assertContains(response, 'team-style-08', count=5)
        self.assertContains(response, 'Contactar al equipo')
        for marker in ('mailto:', 'tel:', 'linkedin.com', 'fa-linkedin-in', 'fa-envelope'):
            self.assertNotContains(response, marker)

    def test_contact_data_shown_only_when_filled(self):
        self.seed_d()
        TeamMember.objects.filter(order=1).update(email='persona@example.com', linkedin_url='https://www.linkedin.com/in/ejemplo')
        TeamMember.objects.filter(order=2).update(phone='+593 00 000 0001')
        response = self.client.get('/equipo/')
        self.assertContains(response, 'mailto:persona@example.com')
        self.assertContains(response, 'https://www.linkedin.com/in/ejemplo')
        self.assertContains(response, 'tel:+593000000001')

    def test_partners_page(self):
        self.seed_d()
        Partner.objects.filter(order=7).update(description='', website='')
        response = self.client.get('/aliados/')
        self.assertContains(response, 'client-box', count=7)
        self.assertContains(response, 'swiper-slide review-style-04"', count=6)
        self.assertContains(response, 'example.com')
        self.assertNotContains(response, 'partner-cobb')

    def test_home_featured_team_and_inactive(self):
        self.seed_d()
        TeamMember.objects.filter(order=2).update(is_active=False)
        response = self.client.get('/')
        self.assertContains(response, 'Nombre del integrante 1')
        self.assertNotContains(response, 'Nombre del integrante 2')
        self.assertNotContains(response, 'Nombre del integrante 4')  # no destacado
        self.assertContains(response, 'id="tab_nine2"')
