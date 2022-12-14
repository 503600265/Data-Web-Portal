# Generated by Django 3.2.7 on 2022-06-30 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tools', '0006_auto_20220630_0911'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('task', models.CharField(max_length=50)),
                ('inloc', models.CharField(max_length=120)),
                ('outloc', models.CharField(max_length=120)),
                ('start_time', models.DateTimeField(auto_now_add=True, verbose_name='start time')),
                ('duration', models.FloatField()),
                ('inloc_size', models.IntegerField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Jobs',
        ),
    ]
