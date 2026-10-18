from django.shortcuts import render


def home(request):
    return render(request, 'gravior/index.html')


def about(request):
    return render(request, 'gravior/nosotros.html')


def classes(request):
    return render(request, 'gravior/genetica.html')


def schedule(request):
    return render(request, 'gravior/servicios.html')


def package(request):
    return render(request, 'gravior/productos.html')


def trainer(request):
    return render(request, 'gravior/equipo.html')


def contact(request):
    return render(request, 'gravior/contacto.html')


def facilities(request):
    return render(request, 'gravior/instalaciones.html')


def partners(request):
    return render(request, 'gravior/aliados.html')


def news(request):
    return render(request, 'gravior/actualidad.html')


def news_detail(request):
    return render(request, 'gravior/actualidad-detalle.html')
