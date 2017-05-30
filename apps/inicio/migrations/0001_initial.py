# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 19:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=70)),
                ('contenido', models.TextField()),
                ('slug', models.SlugField(editable=False)),
                ('imagen', models.ImageField(upload_to='img-noticia/')),
            ],
        ),
        migrations.CreateModel(
            name='NoticiaEstado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField()),
                ('fecha', models.DateField(auto_now_add=True)),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Estado')),
                ('noticia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.Noticia')),
            ],
        ),
        migrations.CreateModel(
            name='Ubigeo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=8)),
                ('nombre', models.CharField(max_length=45)),
            ],
        ),
        migrations.AddField(
            model_name='noticia',
            name='ubigeo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inicio.Ubigeo'),
        ),
    ]