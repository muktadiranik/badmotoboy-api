# Generated by Django 4.0.10 on 2023-04-16 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assaults', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assaultevent',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='assaultevent',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
