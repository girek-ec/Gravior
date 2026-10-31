from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse

from apps.infraestructura.models import Facility, FacilityCategory, FacilityGallery
from apps.productos.models import Product, ProductCategory, ProductDocument, ProductFeature

from .models import SiteConfiguration
from .tests_bloque_b import TempMediaMixin


class SeedCMixin(TempMediaMixin):
    def seed_c(self, *args):
        out = StringIO()
        call_command('seed_bloque_c', *args, stdout=out)
        return out.getvalue()


class SeedBloqueCTests(SeedCMixin, TestCase):
    def test_seed_loads_every_model(self):
        self.seed_c()
        self.assertEqual(ProductCategory.objects.count(), 3)
        self.assertEqual(Product.objects.count(), 3)
        self.assertTrue(all(p.features.count() >= 3 for p in Product.objects.all()))
        self.assertEqual(ProductDocument.objects.count(), 3)
        self.assertEqual(FacilityCategory.objects.count(), 4)
        self.assertEqual(Facility.objects.count(), 12)
        self.assertTrue(all(f.gallery.count() >= 2 for f in Facility.objects.all()))

    def test_visible_texts_are_not_blank(self):
        self.seed_c()
        for product in Product.objects.all():
            for field in ('brand', 'reference', 'summary', 'description', 'application', 'benefits',
                          'inquiry_button_text', 'seo_title', 'seo_description'):
                self.assertTrue(getattr(product, field), (product, field))
        for facility in Facility.objects.all():
            for field in ('summary', 'description', 'public_location'):
                self.assertTrue(getattr(facility, field), (facility, field))
        self.assertFalse(FacilityGallery.objects.filter(caption='').exists())

    def test_sample_pdf(self):
        self.seed_c()
        document = ProductDocument.objects.first()
        self.assertEqual(document.title, 'Documento de ejemplo – reemplazar')
        with document.file.open('rb') as fh:
            self.assertEqual(fh.read(5), b'%PDF-')

    def test_idempotent_and_fill_blanks(self):
        self.seed_c()
        product = Product.objects.get(name='Asesoría técnica')
        product.benefits = ''
        product.summary = 'Resumen del cliente'
        product.save()
        FacilityGallery.objects.filter(caption='Vista general').update(caption='Mi foto')
        Facility.objects.filter(title='Control ambiental').update(public_location='')

        self.seed_c()
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(FacilityGallery.objects.count(), 24)
        self.assertEqual(Product.objects.get(name='Asesoría técnica').benefits, '')

        output = self.seed_c('--fill-blanks')
        product = Product.objects.get(name='Asesoría técnica')
        self.assertTrue(product.benefits)
        self.assertEqual(product.summary, 'Resumen del cliente')
        self.assertTrue(Facility.objects.get(title='Control ambiental').public_location)
        self.assertEqual(FacilityGallery.objects.filter(caption='Mi foto').count(), 12)
        self.assertIn('benefits', output)
        self.assertIn('No había campos vacíos', self.seed_c('--fill-blanks'))


class BlockCModelTests(SeedCMixin, TestCase):
    def test_protect_and_cascade(self):
        self.seed_c()
        category = ProductCategory.objects.get(name='Genética')
        with self.assertRaises(ProtectedError):
            category.delete()
        product = category.products.get()
        with self.assertRaises(ProtectedError):
            product.delete()
        product.documents.all().delete()
        product.delete()
        self.assertFalse(ProductFeature.objects.filter(product_id=product.pk).exists())

        facility_category = FacilityCategory.objects.get(name='Galpones')
        with self.assertRaises(ProtectedError):
            facility_category.delete()
        facility = facility_category.facilities.first()
        facility.delete()
        self.assertFalse(FacilityGallery.objects.filter(facility_id=facility.pk).exists())

    def test_slugs(self):
        category = ProductCategory.objects.create(name='Línea técnica')
        twin = ProductCategory.objects.create(name='Línea técnica')
        self.assertEqual((category.slug, twin.slug), ('linea-tecnica', 'linea-tecnica-2'))
        facility_category = FacilityCategory.objects.create(name='Galpones')
        facility = Facility.objects.create(category=facility_category, title='Área de prueba', summary='x',
                                           main_image='facilities/x.jpg')
        self.assertEqual(facility.slug, 'area-de-prueba')
        facility.title = 'Otro título'
        facility.save()
        self.assertEqual(facility.slug, 'area-de-prueba')


class BlockCAdminTests(SeedCMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(get_user_model().objects.create_superuser('admin-c', 'c@example.com', 'x'))

    def test_changelists_and_forms_load(self):
        self.seed_c()
        for name in ('productos_productcategory', 'productos_product', 'productos_productfeature',
                     'productos_productdocument', 'infraestructura_facilitycategory', 'infraestructura_facility',
                     'infraestructura_facilitygallery'):
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(f'admin:{name}_changelist')).status_code, 200)
                self.assertEqual(self.client.get(reverse(f'admin:{name}_add')).status_code, 200)

    def test_inlines(self):
        self.seed_c()
        product = Product.objects.first()
        response = self.client.get(reverse('admin:productos_product_change', args=[product.pk]))
        self.assertEqual([f.formset.model for f in response.context['inline_admin_formsets']],
                         [ProductFeature, ProductDocument])
        facility = Facility.objects.first()
        response = self.client.get(reverse('admin:infraestructura_facility_change', args=[facility.pk]))
        self.assertEqual([f.formset.model for f in response.context['inline_admin_formsets']], [FacilityGallery])
        self.assertContains(response, facility.gallery.first().image.url)

    def test_admin_groups_order(self):
        labels = [app['app_label'] for app in self.client.get(reverse('admin:index')).context['app_list']]
        self.assertEqual(labels[:7], ['core', 'inicio', 'empresa', 'genetica', 'calidad', 'productos',
                                      'infraestructura'])


class BlockCViewsTests(SeedCMixin, TestCase):
    def test_pages_with_empty_tables(self):
        for path in ('/productos/', '/productos/?categoria=nada', '/instalaciones/', '/'):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)
        self.assertNotContains(self.client.get('/productos/'), 'col pricing-table-style-10')
        self.assertNotContains(self.client.get('/instalaciones/'), 'portfolio-box')

    def test_products_page_and_filter(self):
        self.seed_c()
        response = self.client.get('/productos/')
        self.assertContains(response, 'col pricing-table-style-10', count=3)
        self.assertContains(response, 'Control sanitario')
        self.assertContains(response, 'Destacado', count=2)
        self.assertContains(response, '?categoria=bioseguridad')
        self.assertContains(response, 'Documento de ejemplo – reemplazar', count=3)
        filtered = self.client.get('/productos/?categoria=bioseguridad')
        self.assertContains(filtered, 'col pricing-table-style-10', count=1)
        self.assertNotContains(filtered, 'Asesoría técnica</h2>')

    def test_inactive_items_are_hidden(self):
        self.seed_c()
        ProductFeature.objects.filter(title='Prevención de riesgos').update(is_active=False)
        ProductDocument.objects.update(is_active=False)
        Product.objects.filter(name='Línea genética').update(is_active=False)
        FacilityGallery.objects.update(is_active=False)
        Facility.objects.filter(title='Control ambiental').update(is_active=False)
        response = self.client.get('/productos/')
        self.assertNotContains(response, 'Prevención de riesgos')
        self.assertNotContains(response, '.pdf')
        self.assertNotContains(response, 'Línea genética</h2>')
        facilities = self.client.get('/instalaciones/')
        self.assertNotContains(facilities, 'Control ambiental')
        self.assertContains(facilities, 'data-group="instalacion-', count=11)

    def test_inquiry_button_whatsapp_or_contact(self):
        self.seed_c()
        self.assertContains(self.client.get('/productos/'), reverse('contacto:index'))
        SiteConfiguration.objects.create(company_name='Empresa', logo='site/logo.png', short_description='x',
                                         whatsapp_number='+593 00 000 0000', whatsapp_message='Hola',
                                         copyright_text='Copyright')
        response = self.client.get('/productos/')
        self.assertContains(response, 'https://wa.me/593000000000?text=Hola%20%E2%80%93%20Asesor%C3%ADa%20t%C3%A9cnica')
        SiteConfiguration.objects.update(whatsapp_enabled=False)
        self.assertNotContains(self.client.get('/productos/'), 'wa.me')

    def test_facility_gallery_lightbox(self):
        self.seed_c()
        response = self.client.get('/instalaciones/')
        self.assertContains(response, 'data-filter=".cat-galpones"')
        self.assertContains(response, 'data-group="instalacion-galpones-tecnificados"', count=3)

    def test_home_tabs_include_featured_products(self):
        self.seed_c()
        response = self.client.get('/')
        self.assertContains(response, 'Control sanitario')
        self.assertContains(response, '?categoria=soporte-tecnico')
        self.assertNotContains(response, '?categoria=genetica')  # "Línea genética" no está destacada
