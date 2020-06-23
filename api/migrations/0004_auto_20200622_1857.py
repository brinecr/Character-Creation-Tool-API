# Generated by Django 3.0 on 2020-06-22 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_character_hit_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='attack_power',
            field=models.IntegerField(default='4', editable=False),
        ),
        migrations.AlterField(
            model_name='character',
            name='hit_points',
            field=models.IntegerField(default='10', editable=False),
        ),
    ]
