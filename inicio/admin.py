from django.contrib import admin

from core.admin_utils import image_preview

from .models import Differential, HeroSlide, ProcessStep, Statistic


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('desktop_preview', 'title', 'highlight_text', 'order', 'is_active')
    list_display_links = ('desktop_preview', 'title')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'eyebrow', 'highlight_text', 'description')
    readonly_fields = ('desktop_preview', 'mobile_preview', 'thumbnail_preview')
    fieldsets = (
        ('Textos', {'fields': ('highlight_text', 'eyebrow', 'title', 'description')}),
        ('Imágenes', {'fields': (('desktop_image', 'desktop_preview'), ('mobile_image', 'mobile_preview'),
                                 ('thumbnail', 'thumbnail_preview'))}),
        ('Botones y video', {'fields': (('primary_button_text', 'primary_button_url'),
                                        ('secondary_button_text', 'secondary_button_url'), 'video_url')}),
        ('Publicación', {'fields': ('order', 'is_active')}),
    )

    @admin.display(description='imagen')
    def desktop_preview(self, obj):
        return image_preview(obj.desktop_image)

    @admin.display(description='vista previa')
    def mobile_preview(self, obj):
        return image_preview(obj.mobile_image)

    @admin.display(description='vista previa')
    def thumbnail_preview(self, obj):
        return image_preview(obj.thumbnail)


@admin.register(Differential)
class DifferentialAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_class', 'image_preview', 'show_home', 'show_about', 'order', 'is_active')
    list_editable = ('show_home', 'show_about', 'order', 'is_active')
    list_filter = ('is_active', 'show_home', 'show_about')
    search_fields = ('title', 'description')
    readonly_fields = ('image_preview',)
    fields = ('title', 'description', 'icon_class', ('image', 'image_preview'),
              ('show_home', 'show_about'), 'order', 'is_active')

    @admin.display(description='imagen')
    def image_preview(self, obj):
        return image_preview(obj.image, height=40)


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('title', 'formatted_value', 'show_home', 'show_about', 'order', 'is_active')
    list_editable = ('show_home', 'show_about', 'order', 'is_active')
    list_filter = ('is_active', 'show_home', 'show_about')
    search_fields = ('title', 'description')
    fields = ('title', ('prefix', 'value', 'suffix'), 'description', ('show_home', 'show_about'), 'order', 'is_active')

    @admin.display(description='valor')
    def formatted_value(self, obj):
        return f'{obj.prefix}{obj.value}{obj.suffix}'


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'order', 'is_active')
    list_display_links = ('number', 'title')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
