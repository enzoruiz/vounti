from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    login, logout,
    password_reset, password_reset_done,
    password_reset_confirm, password_reset_complete
)
from .views import (
    RegistroUsuarioView,
    InicioView,
    CambioPasswordView,
    noticia_detalle,
    NoticiaView,
    lista_noticias,
    eliminar_noticia,
    ver_noticia,
    editar_noticia
)

urlpatterns = [
    url(r'^blog$', InicioView.as_view(), name='inicio'),
    url(r'^blog/(?P<slug>[-\w]+)$', noticia_detalle),

    url(r'^lista-noticias$', login_required(lista_noticias),
        name='lista_noticias'),
    url(r'^noticia/$', login_required(NoticiaView.as_view()), name='noticia'),
    url(r'^noticia/(?P<id>[\d]+)/$', login_required(ver_noticia)),
    url(r'^noticia/e/(?P<id>[\d]+)/$', login_required(editar_noticia)),
    url(r'^noticia/d/(?P<id>[\d]+)/$', login_required(eliminar_noticia)),
    url(r'^registro$', RegistroUsuarioView.as_view(), name='registro'),
    url(r'^nueva-password$', login_required(CambioPasswordView.as_view()),
        name='nueva_password'),

    url(r'^login$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^olvide-password/$', password_reset,
        {'template_name': 'reset-password/password_olvidado.html'},
        name='reset_password'),
    url(r'^olvide-password/hecho/$', password_reset_done,
        {'template_name': 'reset-password/password_enviado.html'},
        name='password_reset_done'),
    url(r'^olvide-password/confirmar/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        {'template_name': 'reset-password/password_cambio.html'},
        name='password_reset_confirm'),
    url(r'^olvide-password/completo/$', password_reset_complete,
        {'template_name': 'reset-password/password_confirmacion.html'},
        name='password_reset_complete'),

]
