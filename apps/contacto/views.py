from django.views.generic import TemplateView


class ContactView(TemplateView):
    template_name = 'gravior/contacto.html'
