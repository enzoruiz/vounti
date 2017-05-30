import json
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import Noticia, Ubigeo, Estado, NoticiaEstado
from .forms import NoticiaForm, UsuarioForm
from ..metodos_globales import get_departamentos, get_provincias, get_distritos


class RegistroUsuarioView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'registro.html')

    def post(self, request, *args, **kwargs):
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                User.objects.get(email=request.POST.get("email"))
                msg = 'Usuario ya existe'
                messages.add_message(request, messages.ERROR, msg)
                return redirect('registro')
            except ObjectDoesNotExist:
                user = form.save(commit=False)
                user.password = make_password(request.POST.get("password"))
                user.save()

                user = authenticate(
                            username=request.POST.get('username'),
                            password=request.POST.get('password')
                        )
                login(request, user)

            return redirect("inicio")
        else:
            msg = 'Usuario ya existe'
            messages.add_message(request, messages.ERROR, msg)
            return redirect("registro")


class InicioView(TemplateView):

    def get(self, request, *args, **kwargs):
        noticias = NoticiaEstado.objects.filter(
                                activo=True,
                                estado__valor='1').select_related('noticia')

        return render(request, 'inicio.html', {'noticias': noticias})


def noticia_detalle(request, slug):
    noticia = NoticiaEstado.objects.select_related('noticia', 'estado').get(
                                                        noticia__slug=slug,
                                                        activo=True)
    return render(request, 'noticia_view.html', {'noticia': noticia})


def eliminar_noticia(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    noticia.delete()
    return redirect('lista_noticias')


def lista_noticias(request):
    noticias = NoticiaEstado.objects.filter(activo=True).select_related(
                                                    'noticia',
                                                    'estado')
    return render(request, 'lista_noticias.html', {'noticias': noticias})


class NoticiaView(TemplateView):

    def get(self, request, *args, **kwargs):
        """ 01000000 => pais,
            01010000 => departamento,
            01010100 => provincia,
            01010101 => distrito,
        """
        ubigeo = Ubigeo.objects.all()
        paises = {}
        for elemento in ubigeo:
            if elemento.codigo[2:] == '000000':
                paises[elemento.codigo[:2]] = elemento.nombre

        estados = Estado.objects.all()

        return render(request, 'noticia.html', {
                                        'paises': paises,
                                        'estados': estados
                                    })

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.POST.get('opcion') == 'get_departamentos':
                departamentos = get_departamentos(request.POST.get('codigo'))
                data = json.dumps(departamentos)
                return HttpResponse(data, content_type="application/json")
            elif request.POST.get('opcion') == 'get_provincias':
                provincias = get_provincias(request.POST.get('codigo'))
                data = json.dumps(provincias)
                return HttpResponse(data, content_type="application/json")
            elif request.POST.get('opcion') == 'get_distritos':
                distritos = get_distritos(request.POST.get('codigo'))
                data = json.dumps(distritos)
                return HttpResponse(data, content_type="application/json")
        else:
            form = NoticiaForm(request.POST, request.FILES)
            if form.is_valid():
                noticia = form.save(commit=False)
                noticia.ubigeo = Ubigeo.objects.get(
                                    codigo=request.POST.get('ubigeo')
                                )
                noticia.save()

                noticia_estado = NoticiaEstado()
                noticia_estado.activo = True
                noticia_estado.noticia = noticia
                noticia_estado.estado = get_object_or_404(
                                            Estado,
                                            id=request.POST.get('estado')
                                        )
                noticia_estado.save()

                return redirect("lista_noticias")
            else:
                print(form.errors)
                return redirect("noticia")


def editar_noticia(request, id):
    """ El actual estado de la noticia ('REVISION') pasara a activo=False
        Y se creara un nuevo estado ('PUBLICADO') con activo=True
    """
    if request.method == 'POST':
        noticia = get_object_or_404(Noticia, id=id)
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.ubigeo = Ubigeo.objects.get(
                                codigo=request.POST.get('ubigeo')
                            )
            noticia.save()

            estado = get_object_or_404(Estado, id=request.POST.get('estado'))
            noticia_estado_actual = NoticiaEstado.objects.select_related(
                                            'estado', 'noticia').get(
                                            noticia__id=id, activo=True)

            if (noticia_estado_actual.estado.valor == '2'
                    and estado.valor == '1'):
                noticia_estado_actual.activo = False
                noticia_estado_actual.save()

                noticia_estado_nuevo = NoticiaEstado()
                noticia_estado_nuevo.activo = True
                noticia_estado_nuevo.noticia = noticia
                noticia_estado_nuevo.estado = estado
                noticia_estado_nuevo.save()
    return redirect('lista_noticias')


def ver_noticia(request, id):
    noticia = NoticiaEstado.objects.select_related('noticia', 'estado').get(
                                                                noticia__id=id,
                                                                activo=True
                                                            )

    ubigeo = Ubigeo.objects.all()
    paises = {}
    for elemento in ubigeo:
        if elemento.codigo[2:] == '000000':
            paises[elemento.codigo[:2]] = elemento.nombre

    estados = Estado.objects.all()
    return render(request, 'noticia_edit.html', {
                                'noticia': noticia,
                                'paises': paises,
                                'estados': estados
                            })


class CambioPasswordView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'reset-password/password_cambio.html')

    def post(self, request, *args, **kwargs):
        if (request.POST.get('new_password1')
                == request.POST.get('new_password2')):
            user = User.objects.get(id=request.user.id)
            user.password = make_password(request.POST.get("new_password1"))
            user.save()

            msg = 'Contraseña modificada correctamente'
            messages.add_message(request, messages.SUCCESS, msg)
            return redirect('login')
        else:
            msg = 'Contraseñas deben coincidir'
            messages.add_message(request, messages.ERROR, msg)
            return redirect('nueva_password')
