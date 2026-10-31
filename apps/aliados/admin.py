from django.contrib import admin

from apps.core.admin_utils import image_preview

from .models import Partner


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('logo_preview', 'name', 'alliance_type', 'website', 'is_featured', 'order', 'is_active')
    list_display_links = ('logo_preview', 'name')
    list_editable = ('is_featured', 'order', 'is_active')
    list_filter = ('is_active', 'is_featured', 'alliance_type')
    search_fields = ('name', 'alliance_type', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('logo_preview', 'image_preview')
    fieldsets = (
        ('Aliado', {'fields': ('name', 'slug', ('logo', 'logo_preview'), 'alliance_type', 'description', 'website')}),
        ('Imagen del carrusel', {'fields': (('image', 'image_preview'),)}),
        ('Publicación', {'fields': ('is_featured', 'order', 'is_active')}),
    )

    @admin.display(description='logo')
    def logo_preview(self, obj):
        return image_preview(obj.logo, height=40)

    @admin.display(description='vista previa')
    def image_preview(self, obj):
        return image_preview(obj.image, height=60)
