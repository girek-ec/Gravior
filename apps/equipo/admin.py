from django.contrib import admin

from apps.core.admin_utils import image_preview

from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('photo_preview', 'name', 'position', 'specialty', 'is_featured', 'order', 'is_active')
    list_display_links = ('photo_preview', 'name')
    list_editable = ('is_featured', 'order', 'is_active')
    list_filter = ('is_active', 'is_featured')
    search_fields = ('name', 'position', 'specialty', 'short_bio')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('photo_preview',)
    fieldsets = (
        ('Perfil', {'fields': ('name', 'slug', 'position', 'specialty', 'short_bio', 'biography',
                               ('photo', 'photo_preview'))}),
        ('Datos de contacto (solo con autorización)', {
            'fields': ('email', 'phone', 'linkedin_url'),
            'description': 'Se muestran en la web solo si tienen contenido. Publicar únicamente con aprobación de la persona.',
        }),
        ('Publicación', {'fields': ('is_featured', 'order', 'is_active')}),
    )

    @admin.display(description='foto')
    def photo_preview(self, obj):
        return image_preview(obj.photo, height=60)
