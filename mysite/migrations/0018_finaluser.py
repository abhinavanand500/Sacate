# Generated by Django 3.0.8 on 2020-07-29 11:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0017_auto_20200729_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='finaluser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('superuser', models.CharField(max_length=30, null=True)),
                ('enduser', models.CharField(max_length=30, null=True)),
                ('phone', models.CharField(max_length=30, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('type1', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(max_length=500, null=True)),
                ('done', models.IntegerField(null=True)),
            ],
        ),
    ]
