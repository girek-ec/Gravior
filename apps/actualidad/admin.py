from django.contrib import admin

from apps.core.admin_utils import image_preview

from .models import Post, PostCategory


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'category', 'published_at', 'is_published', 'is_featured')
    list_display_links = ('image_preview', 'title')
    list_editable = ('is_published', 'is_featured')
    list_filter = ('is_published', 'is_featured', 'category')
    search_fields = ('title', 'excerpt', 'content', 'author')
    date_hierarchy = 'published_at'
    list_select_related = ('category',)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('image_preview', 'thumbnail_preview', 'created_at', 'updated_at')
    fieldsets = (
        ('Publicación', {'fields': ('category', 'title', 'slug', 'excerpt', 'content', 'author')}),
        ('Imágenes', {'fields': (('main_image', 'image_preview'), ('thumbnail', 'thumbnail_preview'))}),
        ('Estado', {'fields': ('published_at', 'is_published', 'is_featured')}),
        ('SEO', {'classes': ('collapse',), 'fields': ('seo_title', 'seo_description')}),
        ('Registro', {'classes': ('collapse',), 'fields': ('created_at', 'updated_at')}),
    )

    @admin.display(description='imagen')
    def image_preview(self, obj):
        return image_preview(obj.main_image, height=50)

    @admin.display(description='vista previa')
    def thumbnail_preview(self, obj):
        return image_preview(obj.thumbnail, height=50)
