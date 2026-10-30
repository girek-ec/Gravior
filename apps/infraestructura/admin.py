from django.contrib import admin

from apps.core.admin_utils import image_preview

from .models import Facility, FacilityCategory, FacilityGallery


@admin.register(FacilityCategory)
class FacilityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class FacilityGalleryInline(admin.TabularInline):
    model = FacilityGallery
    extra = 0
    fields = ('image', 'preview', 'caption', 'order', 'is_active')
    readonly_fields = ('preview',)

    @admin.display(description='vista previa')
    def preview(self, obj):
        return image_preview(obj.image, height=50)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'category', 'public_location', 'is_featured', 'order', 'is_active')
    list_display_links = ('image_preview', 'title')
    list_editable = ('is_featured', 'order', 'is_active')
    list_filter = ('is_active', 'is_featured', 'category')
    search_fields = ('title', 'summary', 'description', 'public_location')
    list_select_related = ('category',)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('image_preview',)
    inlines = (FacilityGalleryInline,)
    fieldsets = (
        ('Instalación', {'fields': ('category', 'title', 'slug', 'summary', 'description')}),
        ('Imagen y video', {'fields': (('main_image', 'image_preview'), 'video_url')}),
        ('Ubicación', {
            'fields': ('public_location',),
            'description': 'Solo información publicable. No incluir capacidad exacta, datos estratégicos ni ubicaciones sensibles.',
        }),
        ('Publicación', {'fields': ('is_featured', 'order', 'is_active')}),
    )

    @admin.display(description='imagen')
    def image_preview(self, obj):
        return image_preview(obj.main_image, height=50)


@admin.register(FacilityGallery)
class FacilityGalleryAdmin(admin.ModelAdmin):
    list_display = ('preview', 'facility', 'caption', 'order', 'is_active')
    list_display_links = ('preview', 'caption')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'facility__category', 'facility')
    search_fields = ('caption', 'facility__title')
    list_select_related = ('facility',)

    @admin.display(description='fotografía')
    def preview(self, obj):
        return image_preview(obj.image, height=50)
