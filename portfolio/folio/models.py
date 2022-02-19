import urllib
import uuid
import sys
import tinify
from io import BytesIO
import base64
from django.core.files import File as DjangoFile
import json
from datetime import date
from django.core.files import File
import codecs
from django.core.files.images import get_image_dimensions
import urllib.request
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.db import models
from django.urls import reverse
import os
from PIL import Image
from imagekit import register, ImageSpec
from imagekit.models.fields import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit, Adjust, ResizeToFill, Anchor
from sorl.thumbnail import get_thumbnail

from portfolio import settings
from portfolio.settings import BASE_DIR

API = 'CgTgDvB2gwNbLmksS3Mjm55hS7MQ4HbP'

tinify.key = 'CgTgDvB2gwNbLmksS3Mjm55hS7MQ4HbP'

preview_webp = [(400, 260, '-preview'), (800, 520, '-preview@2x'),
                (1200, 780, '-preview@3x'), (491, 325, '-preview-xl'),
                (982, 650, '-preview-xl@2x'), (1473, 975, '-preview-xl@3x')]

detailed_webp = [(516, 337, ''), (1032, 674, '@2x'),
                 (1548, 1011, '@3x'), (665, 434, '-xl'),
                 (1330, 868, '-xl@2x'), (1995, 1302, '-xl@3x')]

preview_png = [(400, 260, '-preview'), (800, 520, '-preview@2x'),
               (1200, 780, '-preview@3x'), (491, 325, '-preview-xl'),
               (982, 650, '-preview-xl@2x'), (1473, 975, '-preview-xl@3x')]

detailed_png = [(516, 337, ''), (1032, 674, '@2x'),
                (1548, 1011, '@3x'), (665, 434, '-xl'),
                (1330, 868, '-xl@2x'), (1995, 1302, '-xl@3x')]


def get_file_path(instance, filename):
    extension = filename.split('.')[-1]
    new_name = 'avtolider'
    print('fileeeeeeeeename', filename)
    clean_name = filename.split('.')[0]
    filename = "%s.%s" % (new_name, extension)
    date_now = date.today().strftime("%Y/%m/%d").split('/')
    path = 'photos/project_photo/{}/{}/{}'.format(date_now[0], date_now[1], date_now[2])
    print('путь os.path   ', os.path.join(path, filename))
    return os.path.join(path, filename)


class Project(models.Model):

    def find_proprtion(self, instance, new_width, new_height, extension, name, *args,
                       **kwargs):
        filename, file_extension = os.path.splitext(instance.path)
        clean_name = filename.split('\\')[-1]
        nw_name = filename[:filename.rfind('\\')] + '\\' + 'resize\\' + str(clean_name) + str(name)
        folder_resize = filename[:filename.rfind('\\')] + '\\' + 'resize\\'
        try:
            os.mkdir(folder_resize)
        except:
            pass
        save_path = nw_name + '.' + (str(extension)).lower()
        image = Image.open(instance.path)
        relative_name = save_path[save_path.rfind('media'):len(save_path)]
        size = (new_width, new_height)
        res_image = image.resize(size, Image.ANTIALIAS)
        res_image.save(save_path, format=str(extension))
        super().save(*args, **kwargs)
        if sys.getsizeof(extension) == sys.getsizeof('png'):
            try:
                print(sys.getsizeof(extension))
                print(sys.getsizeof('png'))
                print(sys.getsizeof('PNG'))
                print('делаем tinyyyyyyyyyyyyy', extension)
                source = tinify.from_file(save_path)
                # exists = os.path.exists(save_path)
                # if not exists:
                source.to_file(save_path)
            except:
                pass
        else:
            pass
        return relative_name

    def make_resize(self, photo, extension, resolution):
        gallery = {}
        for thumbnail in resolution:
            thumb = self.find_proprtion(photo, thumbnail[0], thumbnail[1], extension=extension, name=thumbnail[2])
            gallery[thumbnail[2]] = thumb
        print(gallery)
        images = os.path.join(os.getcwd())
        print(images)
        return gallery

    def get_file_path(self, filename):
        print('typeeeeeeeeeeee', type(filename))
        extension = filename.split('.')[-1]
        print(extension)
        filename = "%s.%s" % (uuid.uuid4(), extension)
        print(filename)
        print('geeeeeeeeeeeeeeeeet', os.path.join('photos/project_photo/%y/%m/%d'))
        date_now = date.today().strftime("%Y/%m/%d").split('/')
        path = 'photos/project_photo/{}/{}/{}'.format(date_now[0], date_now[1], date_now[2])
        return os.path.join(path, filename)

    id_category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    id_view = models.ForeignKey('View', on_delete=models.CASCADE, verbose_name='Вид')
    id_teamlist = models.ManyToManyField('Team', through='TeamList')
    p_organization = models.CharField(max_length=350, verbose_name='Организация',default=None)
    p_name = models.CharField(max_length=255, verbose_name='Имя проекта')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    p_description = models.TextField(verbose_name='Описание')
    p_i_did = models.CharField(max_length=255, verbose_name='сфера деятельности', blank=True, null=True)
    p_img = models.ImageField( verbose_name='Фото', blank=True, null=True)
    p_img_preview_png = models.JSONField(null=True, blank=True)
    p_img_preview_webp = models.JSONField(null=True, blank=True)
    p_img_large_png = models.JSONField(null=True, blank=True)
    p_img_large_webp = models.JSONField(null=True, blank=True)
    p_link = models.CharField(max_length=255, verbose_name='Ссылка')
    skills = models.ManyToManyField('Skills', blank=True, related_name='project')
    p_git = models.CharField(max_length=255, verbose_name='Github', default=None)
    p_sorting = models.IntegerField(verbose_name='Сортировка')
    p_status = models.IntegerField(verbose_name='Статус')

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)
        webp_preview = self.make_resize(self.p_img, extension='webp', resolution=preview_webp)
        webp_detailed = self.make_resize(self.p_img, extension='webp', resolution=detailed_webp)
        png_preview = self.make_resize(self.p_img, extension='png', resolution=preview_png)
        png_detailed = self.make_resize(self.p_img, extension='png', resolution=detailed_png)
        print(webp_preview)
        print(webp_detailed)
        self.p_img_preview_webp = webp_preview
        self.p_img_large_webp = webp_detailed
        self.p_img_preview_png = png_preview
        self.p_img_large_png = png_detailed
        super().save(*args, **kwargs)

    def __str__(self):
        return self.p_name

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Проект'


class TeamList(models.Model):
    id_project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='Проект')
    id_team = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name='Команда')

    class Meta:
        verbose_name = 'Список команды'

        unique_together = [['id_project', 'id_team']]


class Team(models.Model):
    b_name = models.CharField(max_length=250, verbose_name='Имя')
    b_post = models.CharField(max_length=250, verbose_name='Пост')
    b_link = models.CharField(max_length=250, verbose_name='Ссылка на Github', blank=True)

    def __str__(self):
        return self.b_name

    class Meta:
        verbose_name = 'Программисты'


class Category(models.Model):
    c_name = models.CharField(max_length=100, db_index=True, verbose_name='Имя категории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.c_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class View(models.Model):
    v_name = models.CharField(max_length=150, db_index=True, verbose_name='Имя вида')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.v_name

    class Meta:
        verbose_name = 'Вид'


class Skills(models.Model):
    id_catSkil = models.ForeignKey('CatSkill', on_delete=models.CASCADE, verbose_name='Категория навыка')
    s_name = models.CharField(max_length=250, db_index=True, verbose_name='Навыки')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    s_description = models.CharField(max_length=255, verbose_name='Описание')
    s_img = models.ImageField(upload_to='photos/skill_photo/%y/%m/%d', verbose_name='фото', blank=True, null=True)
    s_quantity = models.IntegerField(verbose_name='Количество')
    s_level = models.IntegerField(verbose_name='Уровень')
    s_sorting = models.IntegerField(verbose_name='Сортировка')
    s_status = models.BooleanField(verbose_name='Статус', default=True)

    # project = models.ManyToManyField('Project', blank=True,related_name='skill')

    def __str__(self):
        return self.s_name

    class Meta:
        verbose_name = 'Навыки'

    def get_absolute_url(self):
        return reverse('skill', kwargs={'pk': self.pk})


class CatSkill(models.Model):
    cs_name = models.CharField(max_length=255, db_index=True, verbose_name='Категория навыков')
    cs_sorting = models.IntegerField(default=0)

    def __str__(self):
        return self.cs_name

    class Meta:
        verbose_name = 'Категория навыков'
