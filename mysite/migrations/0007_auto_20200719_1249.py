# Generated by Django 3.0 on 2020-07-19 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_auto_20200719_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='user',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
