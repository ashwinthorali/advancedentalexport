# Generated by Django 3.2.8 on 2022-12-06 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_videotestimonals'),
    ]

    operations = [
        migrations.AddField(
            model_name='videotestimonals',
            name='video',
            field=models.FileField(null=True, upload_to='Video'),
        ),
    ]
