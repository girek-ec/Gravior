import re

from django import forms

from .models import ContactMessage, ContactReason

CONTROL_CHARS = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')
SINGLE_LINE_FIELDS = ('name', 'company', 'position', 'city', 'phone', 'whatsapp')


class ContactForm(forms.ModelForm):
    """Formulario público de contacto. Validación y limpieza en el servidor."""

    # Campo trampa: invisible para personas; los robots suelen completarlo.
    website = forms.CharField(required=False, label='Sitio web')

    class Meta:
        model = ContactMessage
        fields = ('name', 'company', 'position', 'city', 'email', 'phone', 'whatsapp', 'reason', 'message',
                  'privacy_accepted')
        error_messages = {
            'name': {'required': 'Escribe tu nombre.'},
            'email': {'required': 'Escribe tu correo electrónico.', 'invalid': 'Escribe un correo electrónico válido.'},
            'message': {'required': 'Cuéntanos tu consulta.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reason'].queryset = ContactReason.objects.filter(is_active=True)
        self.fields['reason'].empty_label = 'Motivo de la consulta'
        self.fields['privacy_accepted'].required = True
        self.fields['privacy_accepted'].error_messages['required'] = (
            'Debes aceptar el tratamiento de tus datos para enviar el mensaje.')

    def is_spam(self):
        return bool(self.data.get('website'))

    def clean(self):
        cleaned = super().clean()
        for field in SINGLE_LINE_FIELDS:
            value = cleaned.get(field)
            if value:
                cleaned[field] = ' '.join(CONTROL_CHARS.sub('', value).split())
        message = cleaned.get('message')
        if message:
            message = CONTROL_CHARS.sub('', message).strip()
            if len(message) < 10:
                self.add_error('message', 'La consulta es demasiado corta (mínimo 10 caracteres).')
            cleaned['message'] = message
        return cleaned
