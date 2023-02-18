# Generated by Django 3.2.17 on 2023-02-06 18:07

import app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=512)),
                ('desc', models.TextField()),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('tags', models.CharField(max_length=512)),
                ('image', models.ImageField(upload_to=app.models.file_path_generator_blog, validators=[app.models.validate_image_extension])),
                ('publisher', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='blog', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=512)),
                ('desc', models.TextField()),
                ('icon', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to=app.models.file_path_generator_services, validators=[app.models.validate_image_extension])),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('quote', models.TextField()),
                ('position', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to=app.models.file_path_generator_services, validators=[app.models.validate_image_extension])),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('comment_body', models.TextField()),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('blog', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='app.blog')),
            ],
        ),
    ]