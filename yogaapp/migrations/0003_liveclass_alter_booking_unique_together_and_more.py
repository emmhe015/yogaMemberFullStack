# Generated by Django 4.2.13 on 2024-07-03 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yogaapp', '0002_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiveClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='booking',
            name='yoga_class',
        ),
        migrations.AddField(
            model_name='booking',
            name='live_class',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='yogaapp.liveclass'),
        ),
    ]