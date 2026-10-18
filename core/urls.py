from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    # URLs limpias de GRAVIOR
    path('nosotros/', views.about, name='nosotros'),
    path('genetica/', views.classes, name='genetica'),
    path('servicios/', views.schedule, name='servicios'),
    path('productos/', views.package, name='productos'),
    path('instalaciones/', views.facilities, name='instalaciones'),
    path('equipo/', views.trainer, name='equipo'),
    path('aliados/', views.partners, name='aliados'),
    path('contacto/', views.contact, name='contacto'),
    path('actualidad/', views.news, name='actualidad'),
    path('actualidad/detalle/', views.news_detail, name='actualidad_detalle'),

    # Alias originales de Crafto para mantener navegación sin romper enlaces
    path('demo-gym-and-fitness.html', views.home, name='gym_home'),
    path('demo-gym-and-fitness-about.html', views.about, name='gym_about'),
    path('demo-gym-and-fitness-classes.html', views.classes, name='gym_classes'),
    path('demo-gym-and-fitness-schedule.html', views.schedule, name='gym_schedule'),
    path('demo-gym-and-fitness-package.html', views.package, name='gym_package'),
    path('demo-gym-and-fitness-trainer.html', views.trainer, name='gym_trainer'),
    path('demo-gym-and-fitness-contact.html', views.contact, name='gym_contact'),
    path('demo-corporate-blog.html', views.news, name='corporate_blog'),
    path('demo-corporate-blog-single-clean.html', views.news_detail, name='corporate_blog_detail'),
]
