from django.contrib import admin

from apps.core.admin_utils import SingletonAdminMixin, image_preview

from .models import AboutPage, CorporateValue


@admin.register(AboutPage)
class AboutPageAdmin(SingletonAdminMixin, admin.ModelAdmin):
    readonly_fields = ('main_preview', 'secondary_preview', 'created_at', 'updated_at')
    fieldsets = (
        ('Cabecera', {'fields': ('page_title', 'intro')}),
        ('Contenido corporativo', {'fields': ('company_description', 'value_proposition', 'purpose',
                                              'mission', 'vision', 'client_commitment')}),
        ('Imágenes y video', {'fields': (('main_image', 'main_preview'), ('secondary_image', 'secondary_preview'),
                                         'corporate_video_url')}),
        ('SEO', {'fields': ('seo_title', 'seo_description')}),
        ('Registro', {'classes': ('collapse',), 'fields': ('created_at', 'updated_at')}),
    )

    @admin.display(description='vista previa')
    def main_preview(self, obj):
        return image_preview(obj.main_image)

    @admin.display(description='vista previa')
    def secondary_preview(self, obj):
        return image_preview(obj.secondary_image)


@admin.register(CorporateValue)
class CorporateValueAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'icon_class', 'order', 'is_active')
    list_display_links = ('image_preview', 'name')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    readonly_fields = ('image_preview',)
    fields = ('name', 'description', 'icon_class', ('image', 'image_preview'), 'order', 'is_active')

    @admin.display(description='imagen')
    def image_preview(self, obj):
        return image_preview(obj.image, height=40)
