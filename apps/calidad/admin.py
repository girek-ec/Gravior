from django.contrib import admin

from apps.core.admin_utils import SingletonAdminMixin, image_preview

from .models import QualityArea, QualityPage, QualityStep


@admin.register(QualityPage)
class QualityPageAdmin(SingletonAdminMixin, admin.ModelAdmin):
    readonly_fields = ('main_preview', 'created_at', 'updated_at')
    fieldsets = (
        ('Cabecera', {'fields': ('page_title', 'intro')}),
        ('Contenido', {'fields': ('description', ('main_image', 'main_preview'),
                                  'quality_commitment', 'biosecurity_approach')}),
        ('Llamado a la acción', {'fields': ('cta_text', 'cta_url')}),
        ('SEO', {'fields': ('seo_title', 'seo_description')}),
        ('Registro', {'classes': ('collapse',), 'fields': ('created_at', 'updated_at')}),
    )

    @admin.display(description='vista previa')
    def main_preview(self, obj):
        return image_preview(obj.main_image)


class QualityStepInline(admin.TabularInline):
    model = QualityStep
    extra = 0
    fields = ('number', 'title', 'description', 'order', 'is_active')


@admin.register(QualityArea)
class QualityAreaAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'icon_class', 'order', 'is_active')
    list_display_links = ('image_preview', 'name')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_preview',)
    fields = ('name', 'slug', 'description', 'icon_class', ('image', 'image_preview'), 'order', 'is_active')
    inlines = (QualityStepInline,)

    @admin.display(description='imagen')
    def image_preview(self, obj):
        return image_preview(obj.image, height=50)


@admin.register(QualityStep)
class QualityStepAdmin(admin.ModelAdmin):
    list_display = ('title', 'quality_area', 'number', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'quality_area')
    search_fields = ('title', 'description')
    list_select_related = ('quality_area',)
