from django.db import models
from django.template.defaultfilters import slugify


class Estado(models.Model):
    valor = models.CharField(max_length=1)
    nombre = models.CharField(max_length=45)
    descripcion = models.TextField()


class Ubigeo(models.Model):
    codigo = models.CharField(max_length=8)
    nombre = models.CharField(max_length=45)


class Noticia(models.Model):
    titulo = models.CharField(max_length=70)
    contenido = models.TextField()
    slug = models.SlugField(editable=False)
    imagen = models.ImageField(upload_to='img-noticia/')
    ubigeo = models.OneToOneField(Ubigeo)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Noticia, self).save(*args, **kwargs)


class NoticiaEstado(models.Model):
    activo = models.BooleanField()
    noticia = models.ForeignKey(Noticia)
    estado = models.ForeignKey(Estado)
    fecha = models.DateField(auto_now_add=True)
