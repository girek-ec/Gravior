import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from apps.core.models import CorporateEmail, SiteConfiguration

from .forms import ContactForm
from .services import notify_new_message, rate_limit_exceeded

logger = logging.getLogger(__name__)

SUCCESS_MESSAGE = 'Gracias por escribirnos. Recibimos tu mensaje y te contactaremos pronto.'
RATE_LIMIT_MESSAGE = 'Recibimos varios mensajes desde tu conexión. Intenta nuevamente más tarde o escríbenos por WhatsApp.'


class ContactView(FormView):
    template_name = 'gravior/contacto.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse('contacto:index') + '#formulario-contacto'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if rate_limit_exceeded(request):
            form.add_error(None, RATE_LIMIT_MESSAGE)
            return self.form_invalid(form)
        if form.is_spam():
            # Se responde como si se hubiera enviado, sin guardar ni avisar.
            logger.info('Mensaje de contacto descartado por el campo trampa.')
            messages.success(request, SUCCESS_MESSAGE)
            return redirect(self.get_success_url())
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        message = form.save()
        notify_new_message(message, self.request)
        messages.success(self.request, SUCCESS_MESSAGE)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Revisa los campos marcados para enviar tu mensaje.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        config = SiteConfiguration.get_current()
        channels = list(CorporateEmail.objects.filter(is_active=True))
        if not channels and config and config.main_email:
            channels = [CorporateEmail(label=config.company_name, email=config.main_email)]
        context['contact_channels'] = channels
        return context
