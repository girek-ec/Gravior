from django.contrib import admin

from apps.core.admin_utils import image_preview

from .models import GeneticDocument, GeneticFeature, GeneticLine


class GeneticFeatureInline(admin.TabularInline):
    model = GeneticFeature
    extra = 0
    fields = ('title', 'description', 'icon_class', 'order', 'is_active')


class GeneticDocumentInline(admin.TabularInline):
    model = GeneticDocument
    extra = 0
    fields = ('title', 'document_type', 'file', 'order', 'is_active')


@admin.register(GeneticLine)
class GeneticLineAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'brand_name', 'is_featured', 'order', 'is_active')
    list_display_links = ('image_preview', 'name')
    list_editable = ('is_featured', 'order', 'is_active')
    list_filter = ('is_active', 'is_featured', 'brand_name')
    search_fields = ('name', 'brand_name', 'summary', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_preview', 'secondary_preview', 'brand_logo_preview')
    inlines = (GeneticFeatureInline, GeneticDocumentInline)
    fieldsets = (
        ('Línea', {'fields': ('name', 'slug', 'summary', 'description', 'application')}),
        ('Marca', {'fields': ('brand_name', ('brand_logo', 'brand_logo_preview'))}),
        ('Imágenes', {'fields': (('main_image', 'image_preview'), ('secondary_image', 'secondary_preview'))}),
        ('Publicación', {'fields': ('is_featured', 'order', 'is_active')}),
        ('SEO', {'classes': ('collapse',), 'fields': ('seo_title', 'seo_description')}),
    )

    @admin.display(description='imagen')
    def image_preview(self, obj):
        return image_preview(obj.main_image, height=50)

    @admin.display(description='vista previa')
    def secondary_preview(self, obj):
        return image_preview(obj.secondary_image)

    @admin.display(description='vista previa')
    def brand_logo_preview(self, obj):
        return image_preview(obj.brand_logo, height=40)


@admin.register(GeneticFeature)
class GeneticFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'genetic_line', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'genetic_line')
    search_fields = ('title', 'description')
    list_select_related = ('genetic_line',)


@admin.register(GeneticDocument)
class GeneticDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'genetic_line', 'document_type', 'file', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'document_type', 'genetic_line')
    search_fields = ('title',)
    list_select_related = ('genetic_line',)
