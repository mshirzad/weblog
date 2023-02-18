from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import Service, Testimonial, Faq, Blog, Comment, ContactForm


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


class TestimonialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Testimonial
        fields = '__all__'


class FaqSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faq
        fields = '__all__'


class ContactFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactForm
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class BlogSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True, read_only=True)
    publisher = UserSerializer(read_only=True)


    class Meta:
        model = Blog
        fields = (
            'uid',
            'title',
            'desc',
            'publish_date',
            'tags',
            'image',
            'publisher',
            'comments',
        )
        extra_kwargs = {'comments': {'required': False}} 







