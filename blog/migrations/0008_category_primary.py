# Generated by Django 3.2.8 on 2022-10-13 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_blog_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='primary',
            field=models.BooleanField(default=False),
        ),
    ]
