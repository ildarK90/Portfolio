import urllib
import uuid
import sys
import tinify
from django.dispatch import receiver
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
from django.db.models.signals import pre_save
from django.urls import reverse
import os
from PIL import Image, ImageChops
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_name = self.p_img
        print(self.__original_name)


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
        # super().save(*args, **kwargs)
        # if sys.getsizeof(extension) == sys.getsizeof('png'):
        #     try:
        #         print(sys.getsizeof(extension))
        #         print(sys.getsizeof('png'))
        #         print(sys.getsizeof('PNG'))
        #         print('делаем tinyyyyyyyyyyyyy', extension)
        #         source = tinify.from_file(save_path)
        #         # exists = os.path.exists(save_path)
        #         # if not exists:
        #         source.to_file(save_path)
        #     except:
        #         pass
        # else:
        #     pass
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

    p_name = models.CharField(max_length=255, verbose_name='Имя проекта')
    id_category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    id_view = models.ForeignKey('View', on_delete=models.CASCADE, verbose_name='Вид')
    id_teamlist = models.ManyToManyField('Team', blank=True, related_name='projects', verbose_name='Принимали участие')
    p_organization = models.CharField(max_length=350, verbose_name='Организация', default=None)
    p_description = models.TextField(verbose_name='Кратко о проекте')
    p_i_did = models.TextField(verbose_name='Что было сделано мной')
    p_img = models.ImageField(verbose_name='Фото png 920x600')
    p_img_preview_png = models.JSONField(null=True, blank=True)
    p_img_preview_webp = models.JSONField(null=True, blank=True)
    p_img_large_png = models.JSONField(null=True, blank=True)
    p_img_large_webp = models.JSONField(null=True, blank=True)
    p_link = models.CharField(max_length=255, verbose_name='Ссылка на проект')
    skills = models.ManyToManyField('Skills', related_name='project', verbose_name='Использовал технологии')
    p_git = models.CharField(max_length=255, verbose_name='Ссылка на репозиторий', default=None)
    p_sorting = models.IntegerField(verbose_name='Сортировка', default=0)
    p_status = models.BooleanField(verbose_name='Показать', default=True)

    def save(self, *args, **kwargs):
        if self.p_img:
            print(self.__original_name)
            print('Есть изображение',self.p_img.name,self.__original_name.name)

            if self.__original_name.name != self.p_img.name:
                super(Project, self).save(update_fields=["p_img"])
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
                self.__original_name = self.p_img
            else:
                self.p_img = self.__original_name
                super().save(*args, **kwargs)
                print('загруженное фото',self.p_img.name)
                print('предыдущее фото',self.__original_name)
        else:
            super().save(*args,**kwargs)

    def __str__(self):
        return self.p_name

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = "Проекты"


class Team(models.Model):
    b_name = models.CharField(max_length=250, verbose_name='Имя')
    b_post = models.CharField(max_length=250, verbose_name='Специальность')
    b_link = models.CharField(max_length=250, verbose_name='Ссылка на Github', blank=True)

    def __str__(self):
        return self.b_name

    class Meta:
        verbose_name = 'Программисты'
        verbose_name_plural = "Программисты"


class Category(models.Model):
    c_name = models.CharField(max_length=100, db_index=True, verbose_name='Имя категории')

    def __str__(self):
        return self.c_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class View(models.Model):
    v_name = models.CharField(max_length=150, db_index=True, verbose_name='Имя вида')

    def __str__(self):
        return self.v_name

    class Meta:
        verbose_name = 'Вид'
        verbose_name_plural = "Вид"


class Skills(models.Model):
    id_catSkil = models.ForeignKey('CatSkill', on_delete=models.CASCADE, verbose_name='Категория навыка', related_name='skills')
    s_name = models.CharField(max_length=250, db_index=True, verbose_name='Название')
    s_description = models.CharField(max_length=255, verbose_name='Описание')
    s_img = models.ImageField(upload_to='skills', verbose_name='Иконка svg 123x123px')
    s_quantity = models.IntegerField(verbose_name='Использовал в проектах')
    s_level = models.IntegerField(verbose_name='Уровень владения')
    s_sorting = models.IntegerField(verbose_name='Сортировка')
    s_status = models.BooleanField(verbose_name='Показать', default=True)



    def __str__(self):
        return self.s_name

    class Meta:
        verbose_name = 'Навыки'
        verbose_name_plural = "Навыки"

    def get_absolute_url(self):
        return reverse('skill', kwargs={'pk': self.pk})


class CatSkill(models.Model):
    cs_name = models.CharField(max_length=255, db_index=True, verbose_name='Категория навыков')
    cs_sorting = models.IntegerField(default=0, verbose_name='Сортировка')

    def __str__(self):
        return self.cs_name

    class Meta:
        verbose_name = 'Категория навыков'
        verbose_name_plural = "Категории навыков"
