# Generated by Django 4.0.5 on 2022-06-14 22:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faceid',
            name='description',
        ),
        migrations.RemoveField(
            model_name='faceid',
            name='description2',
        ),
        migrations.RemoveField(
            model_name='faceid',
            name='description3',
        ),
    ]