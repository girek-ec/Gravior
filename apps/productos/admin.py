from django.contrib import admin

from apps.core.admin_utils import image_preview

from .models import Product, ProductCategory, ProductDocument, ProductFeature


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 0
    fields = ('title', 'description', 'order', 'is_active')


class ProductDocumentInline(admin.TabularInline):
    model = ProductDocument
    extra = 0
    fields = ('title', 'document_type', 'file', 'order', 'is_active')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'category', 'reference', 'is_featured', 'order', 'is_active')
    list_display_links = ('image_preview', 'name')
    list_editable = ('is_featured', 'order', 'is_active')
    list_filter = ('is_active', 'is_featured', 'category')
    search_fields = ('name', 'brand', 'reference', 'summary', 'description')
    list_select_related = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_preview',)
    inlines = (ProductFeatureInline, ProductDocumentInline)
    fieldsets = (
        ('Producto', {'fields': ('category', 'name', 'slug', ('brand', 'reference'), 'summary', 'description')}),
        ('Aplicación y beneficios', {'fields': ('application', 'benefits')}),
        ('Imagen', {'fields': (('main_image', 'image_preview'),)}),
        ('Consulta y publicación', {'fields': ('inquiry_button_text', 'is_featured', 'order', 'is_active')}),
        ('SEO', {'classes': ('collapse',), 'fields': ('seo_title', 'seo_description')}),
    )

    @admin.display(description='imagen')
    def image_preview(self, obj):
        return image_preview(obj.main_image, height=50)


@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'product__category')
    search_fields = ('title', 'description', 'product__name')
    list_select_related = ('product',)


@admin.register(ProductDocument)
class ProductDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'document_type', 'file', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'document_type')
    search_fields = ('title', 'product__name')
    list_select_related = ('product',)
