# Generated by Django 4.0.2 on 2022-03-12 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folio', '0007_alter_project_p_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='catskill',
            options={'verbose_name': 'Категория навыков', 'verbose_name_plural': 'Категории навыков'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Проект', 'verbose_name_plural': 'Проекты'},
        ),
        migrations.AlterModelOptions(
            name='skills',
            options={'verbose_name': 'Навыки', 'verbose_name_plural': 'Навыки'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'verbose_name': 'Программисты', 'verbose_name_plural': 'Программисты'},
        ),
        migrations.AlterModelOptions(
            name='view',
            options={'verbose_name': 'Вид', 'verbose_name_plural': 'Вид'},
        ),
        migrations.AlterField(
            model_name='project',
            name='p_img',
            field=models.ImageField(default='photo', upload_to='', verbose_name='Фото'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='p_link',
            field=models.CharField(default=None, max_length=255, verbose_name='Ссылка'),
        ),
    ]
