from django import forms
from .models import Noticia
from django.contrib.auth.models import User


class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ('titulo', 'contenido', 'imagen')


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
