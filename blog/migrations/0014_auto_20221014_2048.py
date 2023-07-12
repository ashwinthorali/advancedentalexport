# Generated by Django 3.2.8 on 2022-10-14 15:18

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_events_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main', models.BooleanField(default=False)),
                ('most_visited', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=True)),
                ('page_name', models.CharField(blank=True, max_length=1256, null=True)),
                ('h1', models.CharField(max_length=156)),
                ('slug', models.CharField(blank=True, max_length=1256, null=True)),
                ('keyword', models.CharField(max_length=156)),
                ('description', models.CharField(max_length=900)),
                ('title', models.CharField(max_length=156)),
                ('breadcrumb', models.CharField(max_length=156)),
                ('canonical', models.CharField(default='https://thegrandindianroute.com/', max_length=900)),
                ('og_type', models.CharField(max_length=156)),
                ('og_card', models.CharField(max_length=156)),
                ('og_site', models.CharField(max_length=156)),
                ('image', models.ImageField(upload_to='SEO')),
                ('updated', models.DateField(auto_now=True)),
                ('published', models.DateField()),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('edits', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='blog',
            name='author',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='blog_banner_lg',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='blog_banner_sm',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='category',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='tag',
        ),
        migrations.CreateModel(
            name='SubProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main', models.BooleanField(default=False)),
                ('most_visited', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=True)),
                ('page_name', models.CharField(blank=True, max_length=1256, null=True)),
                ('h1', models.CharField(max_length=156)),
                ('slug', models.CharField(blank=True, max_length=1256, null=True)),
                ('keyword', models.CharField(max_length=156)),
                ('description', models.CharField(max_length=900)),
                ('title', models.CharField(max_length=156)),
                ('breadcrumb', models.CharField(max_length=156)),
                ('canonical', models.CharField(default='https://thegrandindianroute.com/', max_length=900)),
                ('og_type', models.CharField(max_length=156)),
                ('og_card', models.CharField(max_length=156)),
                ('og_site', models.CharField(max_length=156)),
                ('image', models.ImageField(upload_to='SEO')),
                ('updated', models.DateField(auto_now=True)),
                ('blog_banner_lg', models.ImageField(blank=True, null=True, upload_to='Page Data')),
                ('blog_banner_sm', models.ImageField(blank=True, null=True, upload_to='Page Data')),
                ('published', models.DateField()),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('edits', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.author')),
                ('category', models.ManyToManyField(to='blog.Category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.product')),
                ('tag', models.ManyToManyField(to='blog.Tags')),
            ],
        ),
    ]