from datetime import timedelta
from io import StringIO
from unittest import mock

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.core.management import call_command
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.actualidad.models import Post, PostCategory
from apps.contacto.models import ContactMessage, ContactReason

from .models import CorporateEmail, SiteConfiguration
from .tests_bloque_b import TempMediaMixin

VALID_DATA = {
    'name': 'Persona de prueba', 'email': 'persona@example.com', 'company': 'Empresa',
    'message': 'Quisiera recibir información sobre las soluciones disponibles.', 'privacy_accepted': 'on',
}


class SeedEMixin(TempMediaMixin):
    def seed_e(self, *args):
        out = StringIO()
        call_command('seed_bloque_e', *args, stdout=out)
        return out.getvalue()


class SeedBloqueETests(SeedEMixin, TestCase):
    def test_seed_loads_posts_and_reasons(self):
        self.seed_e()
        self.assertEqual(PostCategory.objects.count(), 4)
        self.assertEqual(Post.objects.count(), 6)
        self.assertEqual(Post.objects.published().count(), 6)
        self.assertEqual(ContactReason.objects.count(), 5)
        self.assertEqual(ContactMessage.objects.count(), 0)
        for post in Post.objects.all():
            for field in ('excerpt', 'content', 'author', 'seo_title', 'seo_description'):
                self.assertTrue(getattr(post, field), field)
            self.assertGreaterEqual(len(post.paragraphs), 2)

    def test_idempotent_and_fill_blanks(self):
        self.seed_e()
        Post.objects.filter(title__startswith='Claves').update(author='', excerpt='Resumen del cliente')
        self.seed_e()
        self.assertEqual(Post.objects.count(), 6)
        output = self.seed_e('--fill-blanks')
        post = Post.objects.get(title__startswith='Claves')
        self.assertEqual(post.author, 'Equipo GRAVIOR')
        self.assertEqual(post.excerpt, 'Resumen del cliente')
        self.assertIn('author', output)
        self.assertIn('No había campos vacíos', self.seed_e('--fill-blanks'))


class ActualidadViewsTests(SeedEMixin, TestCase):
    def test_empty_tables(self):
        self.assertEqual(self.client.get('/actualidad/').status_code, 200)
        self.assertNotContains(self.client.get('/actualidad/'), 'class="grid-item"')
        self.assertEqual(self.client.get('/actualidad/cualquiera/').status_code, 404)

    def test_list_filter_and_pagination(self):
        self.seed_e()
        response = self.client.get('/actualidad/')
        self.assertContains(response, 'class="grid-item"', count=6)
        self.assertNotContains(response, 'fa-heart')
        self.assertContains(self.client.get('/actualidad/?categoria=bioseguridad'), 'class="grid-item"', count=2)
        category = PostCategory.objects.get(name='Genética')
        for i in range(10):
            Post.objects.create(category=category, title=f'Nota {i}', excerpt='x', content='Texto de la nota.',
                                main_image='blog/x.jpg')
        response = self.client.get('/actualidad/')
        self.assertContains(response, 'class="grid-item"', count=9)
        self.assertContains(response, 'pagination-style-01')
        self.assertContains(self.client.get('/actualidad/?page=2'), 'class="grid-item"', count=7)

    def test_only_current_posts_are_public(self):
        self.seed_e()
        future = Post.objects.get(title__startswith='Claves')
        future.published_at = timezone.now() + timedelta(days=3)
        future.save()
        draft = Post.objects.get(title__startswith='Bioseguridad:')
        draft.is_published = False
        draft.save()
        PostCategory.objects.filter(name='Tecnología').update(is_active=False)
        response = self.client.get('/actualidad/')
        self.assertContains(response, 'class="grid-item"', count=3)
        for post in (future, draft, Post.objects.get(category__name='Tecnología')):
            self.assertEqual(self.client.get(post.get_absolute_url()).status_code, 404)

    def test_detail_page(self):
        self.seed_e()
        post = Post.objects.get(title__startswith='Claves')
        response = self.client.get(post.get_absolute_url())
        self.assertContains(response, f'<title>{post.seo_title}</title>', html=True)
        self.assertContains(response, post.excerpt)
        self.assertContains(response, 'Artículos relacionados')
        self.assertContains(response, 'sharer.php?u=http%3A%2F%2Ftestserver%2Factualidad%2F')
        for leftover in ('Morbi ultricies', 'contact-form.php', '17 July 2020', 'Post Comment'):
            self.assertNotContains(response, leftover)

    def test_content_is_escaped(self):
        self.seed_e()
        post = Post.objects.get(title__startswith='Claves')
        post.content = 'Primer párrafo con <b>negrita</b>\n\n<script>alert(1)</script> segundo'
        post.save()
        response = self.client.get(post.get_absolute_url())
        self.assertNotContains(response, '<script>alert(1)</script>')
        self.assertContains(response, '&lt;b&gt;negrita&lt;/b&gt;')
        self.assertContains(response, '&lt;script&gt;alert(1)&lt;/script&gt;')


@override_settings(CONTACT_RATE_LIMIT=3, CONTACT_RATE_WINDOW=3600)
class ContactFormTests(TestCase):
    def setUp(self):
        cache.clear()
        self.reason = ContactReason.objects.create(name='Productos', order=1)
        ContactReason.objects.create(name='Inactivo', order=2, is_active=False)
        CorporateEmail.objects.create(label='Comercial', email='comercial@example.com',
                                      email_type=CorporateEmail.EmailType.COMMERCIAL)
        CorporateEmail.objects.create(label='Información', email='info@example.com',
                                      email_type=CorporateEmail.EmailType.INFO)

    def post(self, **overrides):
        data = {**VALID_DATA, 'reason': self.reason.pk, **overrides}
        return self.client.post(reverse('contacto:index'), data)

    def test_valid_submission_saves_and_notifies(self):
        response = self.post(name='  Persona \x07 de   prueba ')
        self.assertRedirects(response, reverse('contacto:index') + '#formulario-contacto', fetch_redirect_response=False)
        message = ContactMessage.objects.get()
        self.assertEqual(message.name, 'Persona de prueba')
        self.assertTrue(message.privacy_accepted)
        self.assertEqual(message.reason, self.reason)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['comercial@example.com'])
        self.assertEqual(mail.outbox[0].reply_to, ['persona@example.com'])
        self.assertContains(self.client.get(reverse('contacto:index')), 'Gracias por escribirnos')

    def test_validation_errors(self):
        response = self.post(email='no-es-correo', message='corto', privacy_accepted='')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Escribe un correo electrónico válido.')
        self.assertContains(response, 'mínimo 10 caracteres')
        self.assertContains(response, 'Debes aceptar el tratamiento de tus datos')
        self.assertFalse(ContactMessage.objects.exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_inactive_reason_is_rejected(self):
        inactive = ContactReason.objects.get(name='Inactivo')
        response = self.post(reason=inactive.pk)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ContactMessage.objects.exists())

    def test_honeypot_discards_silently(self):
        response = self.post(website='https://spam.example.com')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ContactMessage.objects.exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_rate_limit_per_ip(self):
        for _ in range(3):
            self.assertEqual(self.post().status_code, 302)
        response = self.post()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Intenta nuevamente más tarde')
        self.assertEqual(ContactMessage.objects.count(), 3)
        other_ip = self.client.post(reverse('contacto:index'), {**VALID_DATA, 'reason': self.reason.pk},
                                    REMOTE_ADDR='10.0.0.9')
        self.assertEqual(other_ip.status_code, 302)

    def test_csrf_is_required(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse('contacto:index'), VALID_DATA)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(ContactMessage.objects.exists())

    def test_email_failure_does_not_expose_internal_addresses(self):
        with mock.patch('apps.contacto.services.EmailMessage.send', side_effect=OSError('smtp caído')),                 self.assertLogs('apps.contacto.services', level='ERROR'):
            response = self.post()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ContactMessage.objects.exists())
        page = self.client.get(reverse('contacto:index'))
        self.assertNotContains(page, 'smtp caído')

    def test_recipient_fallbacks(self):
        CorporateEmail.objects.filter(email_type=CorporateEmail.EmailType.COMMERCIAL).delete()
        self.post()
        self.assertEqual(mail.outbox[-1].to, ['info@example.com'])
        CorporateEmail.objects.all().delete()
        SiteConfiguration.objects.create(company_name='Empresa', logo='site/l.png', short_description='x',
                                         whatsapp_number='+593 00 000 0000', copyright_text='c',
                                         main_email='general@example.com')
        self.post(email='otra@example.com')
        self.assertEqual(mail.outbox[-1].to, ['general@example.com'])


class ContactPageTests(TestCase):
    def test_page_without_configuration(self):
        response = self.client.get(reverse('contacto:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'id="tab_eight1"')
        self.assertContains(response, 'name="privacy_accepted"')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertNotContains(response, 'class="btn btn-medium btn-round-edge btn-dark-gray btn-slide-right submit"')

    def test_page_shows_site_data(self):
        SiteConfiguration.objects.create(
            company_name='Empresa', logo='site/l.png', short_description='x', copyright_text='c',
            whatsapp_number='+593 00 000 0000', phone='+593 00 000 0001', address='Dirección de prueba',
            business_hours='Horario de prueba', google_maps_url='https://maps.example.com/lugar')
        CorporateEmail.objects.create(label='Comercial', email='comercial@example.com')
        response = self.client.get(reverse('contacto:index'))
        for text in ('id="tab_eight1"', 'mailto:comercial@example.com', 'tel:+593000000001',
                     'https://wa.me/593000000000', 'https://maps.example.com/lugar', 'Horario de prueba'):
            self.assertContains(response, text)


class ContactAdminTests(TestCase):
    def setUp(self):
        self.client.force_login(get_user_model().objects.create_superuser('admin-e', 'e@example.com', 'x'))
        self.message = ContactMessage.objects.create(name='Persona', email='p@example.com',
                                                     message='Mensaje de prueba suficiente.', privacy_accepted=True)

    def test_readonly_and_no_add(self):
        self.assertEqual(self.client.get(reverse('admin:contacto_contactmessage_add')).status_code, 403)
        url = reverse('admin:contacto_contactmessage_change', args=[self.message.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_read)  # abrir el mensaje lo marca como leído
        self.client.post(url, {'name': 'Cambiado', 'is_read': 'on', 'is_answered': 'on'})
        self.message.refresh_from_db()
        self.assertEqual(self.message.name, 'Persona')
        self.assertTrue(self.message.is_answered)

    def test_changelist_filters_and_actions(self):
        changelist = reverse('admin:contacto_contactmessage_changelist')
        self.assertEqual(self.client.get(changelist + '?is_read__exact=0').status_code, 200)
        self.client.post(changelist, {'action': 'mark_archived', '_selected_action': [self.message.pk]})
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_archived)
        self.client.post(changelist, {'action': 'mark_answered', '_selected_action': [self.message.pk]})
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_answered and self.message.is_read)

    def test_other_changelists(self):
        for name in ('actualidad_postcategory', 'actualidad_post', 'contacto_contactreason'):
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(f'admin:{name}_changelist')).status_code, 200)
                self.assertEqual(self.client.get(reverse(f'admin:{name}_add')).status_code, 200)
