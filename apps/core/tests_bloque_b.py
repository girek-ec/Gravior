import shutil
import tempfile
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.db.models import ProtectedError
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.calidad.models import QualityArea, QualityPage, QualityStep
from apps.empresa.models import AboutPage, CorporateValue
from apps.genetica.models import GeneticDocument, GeneticFeature, GeneticLine

from .validators import validate_pdf_signature


class TempMediaMixin:
    def setUp(self):
        super().setUp()
        media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, media, ignore_errors=True)
        override = override_settings(MEDIA_ROOT=media)
        override.enable()
        self.addCleanup(override.disable)

    def seed(self, *args):
        out = StringIO()
        call_command('seed_bloque_b', *args, stdout=out)
        return out.getvalue()


class SeedBloqueBTests(TempMediaMixin, TestCase):
    def test_seed_loads_every_model(self):
        self.seed()
        self.assertEqual(AboutPage.objects.count(), 1)
        self.assertEqual(QualityPage.objects.count(), 1)
        self.assertGreaterEqual(CorporateValue.objects.count(), 3)
        self.assertEqual(GeneticLine.objects.count(), 2)
        self.assertTrue(all(line.features.count() >= 3 for line in GeneticLine.objects.all()))
        self.assertEqual(QualityArea.objects.count(), 7)
        self.assertTrue(all(area.steps.count() >= 3 for area in QualityArea.objects.all()))

    def test_visible_texts_are_not_blank(self):
        self.seed()
        about = AboutPage.objects.get()
        for field in ('page_title', 'intro', 'company_description', 'purpose', 'mission', 'vision',
                      'value_proposition', 'client_commitment', 'seo_title', 'seo_description'):
            self.assertTrue(getattr(about, field), field)
        page = QualityPage.objects.get()
        for field in ('page_title', 'intro', 'description', 'quality_commitment', 'biosecurity_approach',
                      'cta_text', 'cta_url', 'seo_title', 'seo_description'):
            self.assertTrue(getattr(page, field), field)

    def test_cobb_without_logo_and_sample_pdf(self):
        self.seed()
        cobb = GeneticLine.objects.get(brand_name='Cobb')
        self.assertFalse(cobb.brand_logo)
        document = cobb.documents.get()
        self.assertEqual(document.title, 'Documento de ejemplo – reemplazar')
        with document.file.open('rb') as fh:
            self.assertEqual(fh.read(5), b'%PDF-')

    def test_idempotent_and_fill_blanks(self):
        self.seed()
        about = AboutPage.objects.get()
        about.mission = ''
        about.vision = 'Visión del cliente'
        about.save()
        line = GeneticLine.objects.get(name='Genética Cobb')
        line.name = 'Nombre editado'
        line.save()
        GeneticFeature.objects.filter(title='Uniformidad').update(icon_class='')
        QualityStep.objects.filter(title='Ventilación').update(number='')

        self.seed()
        self.assertEqual(GeneticLine.objects.count(), 2)
        self.assertEqual(AboutPage.objects.get().mission, '')

        output = self.seed('--fill-blanks')
        about = AboutPage.objects.get()
        self.assertTrue(about.mission)
        self.assertEqual(about.vision, 'Visión del cliente')
        self.assertEqual(QualityStep.objects.get(title='Ventilación').number, '02')
        self.assertIn('mission', output)
        # La línea renombrada por el cliente no se toca (no coincide por clave).
        self.assertEqual(GeneticFeature.objects.get(title='Uniformidad').icon_class, '')
        self.assertEqual(GeneticLine.objects.count(), 2)
        self.assertIn('No había campos vacíos', self.seed('--fill-blanks'))


class BlockBModelTests(TempMediaMixin, TestCase):
    def test_singletons_reject_second_instance(self):
        self.seed()
        with self.assertRaises(ValidationError):
            AboutPage(page_title='Otra').full_clean()
        with self.assertRaises(ValidationError):
            QualityPage(page_title='Otra').full_clean()

    def test_slugs_are_generated_unique_and_stable(self):
        area = QualityArea.objects.create(name='Área técnica', description='x')
        twin = QualityArea.objects.create(name='Área técnica', description='y')
        self.assertEqual(area.slug, 'area-tecnica')
        self.assertEqual(twin.slug, 'area-tecnica-2')
        area.name = 'Otro nombre'
        area.save()
        self.assertEqual(area.slug, 'area-tecnica')

    def test_documents_protect_their_line_and_features_cascade(self):
        self.seed()
        line = GeneticLine.objects.get(name='Genética Cobb')
        with self.assertRaises(ProtectedError):
            line.delete()
        line.documents.all().delete()
        line.delete()
        self.assertFalse(GeneticFeature.objects.filter(genetic_line_id=line.pk).exists())

    def test_pdf_signature_validator(self):
        with self.assertRaises(ValidationError):
            validate_pdf_signature(SimpleUploadedFile('falso.pdf', b'no es un pdf'))
        validate_pdf_signature(SimpleUploadedFile('ok.pdf', b'%PDF-1.4 contenido'))


class BlockBAdminTests(TempMediaMixin, TestCase):
    def setUp(self):
        super().setUp()
        user = get_user_model().objects.create_superuser('admin-b', 'b@example.com', 'x')
        self.client.force_login(user)

    def test_changelists_and_forms_load(self):
        self.seed()
        for name in ('empresa_corporatevalue', 'genetica_geneticline', 'genetica_geneticfeature',
                     'genetica_geneticdocument', 'calidad_qualityarea', 'calidad_qualitystep'):
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(f'admin:{name}_changelist')).status_code, 200)
                self.assertEqual(self.client.get(reverse(f'admin:{name}_add')).status_code, 200)

    def test_inlines(self):
        self.seed()
        line = GeneticLine.objects.first()
        response = self.client.get(reverse('admin:genetica_geneticline_change', args=[line.pk]))
        models = [formset.formset.model for formset in response.context['inline_admin_formsets']]
        self.assertEqual(models, [GeneticFeature, GeneticDocument])
        area = QualityArea.objects.first()
        response = self.client.get(reverse('admin:calidad_qualityarea_change', args=[area.pk]))
        self.assertEqual([f.formset.model for f in response.context['inline_admin_formsets']], [QualityStep])

    def test_singleton_admin(self):
        for name, model in (('empresa_aboutpage', AboutPage), ('calidad_qualitypage', QualityPage)):
            with self.subTest(name=name):
                self.assertRedirects(self.client.get(reverse(f'admin:{name}_changelist')),
                                     reverse(f'admin:{name}_add'))
        self.seed()
        for name, model in (('empresa_aboutpage', AboutPage), ('calidad_qualitypage', QualityPage)):
            obj = model.objects.get()
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(f'admin:{name}_add')).status_code, 403)
                self.assertEqual(self.client.get(reverse(f'admin:{name}_delete', args=[obj.pk])).status_code, 403)

    def test_admin_groups_order(self):
        response = self.client.get(reverse('admin:index'))
        labels = [app['app_label'] for app in response.context['app_list']]
        self.assertEqual(labels[:5], ['core', 'inicio', 'empresa', 'genetica', 'calidad'])


class BlockBViewsTests(TempMediaMixin, TestCase):
    PAGES = ('/', '/nosotros/', '/genetica/', '/calidad-bioseguridad/')

    def test_pages_with_empty_tables(self):
        for path in self.PAGES:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
        self.assertNotContains(self.client.get('/calidad-bioseguridad/'), 'tab-pane')
        self.assertNotContains(self.client.get('/genetica/'), 'interactive-banner-style-04')
        self.assertNotContains(self.client.get('/nosotros/'), 'rotate-box-style-01')

    def test_pages_with_seeded_content(self):
        self.seed()
        about = AboutPage.objects.get()
        response = self.client.get('/nosotros/')
        self.assertContains(response, about.value_proposition)
        self.assertContains(response, f'<title>{about.seo_title}</title>', html=True)
        self.assertContains(response, 'Sostenibilidad')

        response = self.client.get('/genetica/')
        self.assertContains(response, 'Genética Cobb')
        self.assertContains(response, 'Documento de ejemplo – reemplazar')
        self.assertContains(response, '.pdf')

        response = self.client.get('/calidad-bioseguridad/')
        self.assertContains(response, 'Evaluación de riesgos')
        self.assertContains(response, 'data-to="7"')

        response = self.client.get('/')
        self.assertContains(response, about.company_description)
        self.assertContains(response, 'id="tab_eight5"')
        self.assertContains(response, 'accordion-style-07-03')

    def test_inactive_elements_and_optional_fields(self):
        self.seed()
        GeneticFeature.objects.filter(title='Robustez').update(is_active=False)
        GeneticDocument.objects.update(is_active=False)
        QualityStep.objects.filter(title='Ventilación').update(is_active=False)
        AboutPage.objects.update(purpose='', vision='', secondary_image='', corporate_video_url='', seo_title='')
        QualityPage.objects.update(cta_text='', cta_url='')
        genetics = self.client.get('/genetica/')
        self.assertNotContains(genetics, 'Robustez')
        self.assertNotContains(genetics, '.pdf')
        self.assertNotContains(self.client.get('/calidad-bioseguridad/'), 'Ventilación')
        about = self.client.get('/nosotros/')
        self.assertEqual(about.status_code, 200)
        self.assertContains(about, 'cfXHhfNy7tU')  # video de la maqueta como respaldo

    def test_corporate_video_url_replaces_mockup_video(self):
        self.seed()
        AboutPage.objects.update(corporate_video_url='https://www.youtube.com/watch?v=VIDEO_PROPIO')
        response = self.client.get('/nosotros/')
        self.assertContains(response, 'VIDEO_PROPIO')
