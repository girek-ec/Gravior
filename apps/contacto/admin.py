from django.contrib import admin, messages

from .models import ContactMessage, ContactReason

SUBMITTED_FIELDS = ('name', 'company', 'position', 'city', 'phone', 'whatsapp', 'email', 'reason', 'message',
                    'privacy_accepted', 'created_at')


@admin.register(ContactReason)
class ContactReasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Bandeja de mensajes: los datos enviados son de solo lectura; solo se gestiona el estado."""

    list_display = ('created_at', 'name', 'email', 'company', 'reason', 'is_read', 'is_answered', 'is_archived')
    list_display_links = ('created_at', 'name')
    list_filter = ('is_read', 'is_answered', 'is_archived', 'reason', 'created_at')
    search_fields = ('name', 'email', 'company', 'city', 'message')
    date_hierarchy = 'created_at'
    list_select_related = ('reason',)
    readonly_fields = SUBMITTED_FIELDS
    fieldsets = (
        ('Datos enviados', {'fields': SUBMITTED_FIELDS}),
        ('Seguimiento', {'fields': ('is_read', 'is_answered', 'is_archived')}),
    )
    actions = ('mark_read', 'mark_unread', 'mark_answered', 'mark_archived', 'mark_unarchived')

    def has_add_permission(self, request):
        return False  # los mensajes llegan solo desde el formulario de la web

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.method == 'GET':
            ContactMessage.objects.filter(pk=object_id, is_read=False).update(is_read=True)
        return super().change_view(request, object_id, form_url, extra_context)

    def _mark(self, request, queryset, label, **values):
        updated = queryset.update(**values)
        self.message_user(request, f'{updated} mensaje(s) marcado(s) como {label}.', messages.SUCCESS)

    @admin.action(description='Marcar como leídos')
    def mark_read(self, request, queryset):
        self._mark(request, queryset, 'leídos', is_read=True)

    @admin.action(description='Marcar como no leídos')
    def mark_unread(self, request, queryset):
        self._mark(request, queryset, 'no leídos', is_read=False)

    @admin.action(description='Marcar como respondidos')
    def mark_answered(self, request, queryset):
        self._mark(request, queryset, 'respondidos', is_answered=True, is_read=True)

    @admin.action(description='Archivar')
    def mark_archived(self, request, queryset):
        self._mark(request, queryset, 'archivados', is_archived=True)

    @admin.action(description='Quitar de archivados')
    def mark_unarchived(self, request, queryset):
        self._mark(request, queryset, 'no archivados', is_archived=False)
