# Generated by Django 4.2.13 on 2024-07-13 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yogaapp', '0006_delete_yogaclass_liveclass_featured_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]