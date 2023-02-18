import uuid, os

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.utils.timezone import now

def file_path_generator_services(instance, filename):
    extension = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'

    return os.path.join(f'servicesAndTestimonials/', filename)

def file_path_generator_blog(instance, filename):
    extension = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'

    return os.path.join(f'blog/', filename)

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png', '.jpeg', '.svg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension')


class Service(models.Model):

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=512)
    desc = models.TextField()
    icon = models.CharField(max_length=255)
    image = models.ImageField(upload_to=file_path_generator_services, validators=[validate_image_extension])

    
    def __str__(self) -> str:
        return f'{self.title}'

class Testimonial(models.Model):

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    quote = models.TextField()
    position = models.CharField(max_length=255)
    image = models.ImageField(upload_to=file_path_generator_services, validators=[validate_image_extension])

    
    def __str__(self) -> str:
        return f'{self.name} , {self.position}'

class Faq(models.Model):

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField()
    answer  = models.TextField()

    
    def __str__(self) -> str:
        return f'{self.question}'

class Blog(models.Model):

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=512)
    desc = models.TextField()
    publisher = models.ForeignKey(User, related_name='blog', on_delete=models.CASCADE)
    publish_date = models.DateTimeField(default=now, editable=False)
    tags = models.CharField(max_length=512)
    image = models.ImageField(upload_to=file_path_generator_blog, validators=[validate_image_extension])

    
    def __str__(self) -> str:
        return f'{self.title}, {self.desc}, {self.publisher} , {self.publish_date}, {self.tags}, {self.uid}'


class Comment(models.Model):

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    comment_body = models.TextField()
    publish_date = models.DateTimeField(default=now, editable=False)
    blog = models.ForeignKey(Blog, related_name='comment', on_delete=CASCADE)

    
    def __str__(self) -> str:
        return f'{self.name} , {self.publish_date}'


class ContactForm(models.Model):

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField()

    
    def __str__(self) -> str:
        return f'{self.name} , {self.subject}'