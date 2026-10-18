from django.contrib import admin

from .admin_utils import SingletonAdminMixin, image_preview
from .models import CallToAction, CorporateEmail, SiteConfiguration, SocialNetwork


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonAdminMixin, admin.ModelAdmin):
    """Singleton: una sola configuración, sin opción de crear otra ni de borrarla."""

    readonly_fields = ('logo_preview', 'logo_white_preview', 'isotype_preview', 'favicon_preview',
                       'created_at', 'updated_at')
    fieldsets = (
        ('Identidad', {
            'fields': ('company_name', 'legal_name', 'short_description',
                       ('logo', 'logo_preview'), ('logo_white', 'logo_white_preview'),
                       ('isotype', 'isotype_preview'), ('favicon', 'favicon_preview')),
        }),
        ('Contacto y ubicación', {
            'fields': ('phone', 'main_email', 'address', ('city', 'province', 'country'),
                       'business_hours', 'google_maps_url'),
        }),
        ('WhatsApp', {
            'fields': ('whatsapp_enabled', 'whatsapp_number', 'whatsapp_message'),
        }),
        ('Pie de página y SEO', {
            'fields': ('copyright_text', 'default_seo_title', 'default_seo_description'),
        }),
        ('Registro', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )

    @admin.display(description='vista previa')
    def logo_preview(self, obj):
        return image_preview(obj.logo)

    @admin.display(description='vista previa')
    def logo_white_preview(self, obj):
        return image_preview(obj.logo_white)

    @admin.display(description='vista previa')
    def isotype_preview(self, obj):
        return image_preview(obj.isotype)

    @admin.display(description='vista previa')
    def favicon_preview(self, obj):
        return image_preview(obj.favicon, height=32)


@admin.register(CorporateEmail)
class CorporateEmailAdmin(admin.ModelAdmin):
    list_display = ('label', 'email', 'email_type', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'email_type')
    search_fields = ('label', 'email')


@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'icon_class', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'url')


@admin.register(CallToAction)
class CallToActionAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'button_text', 'button_url', 'image_preview', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = ('title', 'code', 'text', 'button_text')
    readonly_fields = ('image_preview',)
    fields = ('code', 'title', 'text', 'button_text', 'button_url', ('image', 'image_preview'), 'is_active')

    @admin.display(description='imagen')
    def image_preview(self, obj):
        return image_preview(obj.image)
