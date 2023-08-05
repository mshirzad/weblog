import json
import os
import IP2Location

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.core.mail import send_mail

from app.models import Service, Testimonial, Faq, Blog, Comment, ContactForm
from app.serializers import ServiceSerializer, TestimonialSerializer, FaqSerializer, BlogSerializer, CommentSerializer, ContactFormSerializer

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


def home(request):
    return render(request, 'app/index.html')

def blog(request):
    all_blogs = Blog.objects.all().order_by('publish_date')[::-1]
    recent_blogs = all_blogs[:5]

    return render(request, 'app/blog.html', context={'all_blogs': all_blogs, 'recent_blogs': recent_blogs})

def blog_details(request):
    context = {}
    try:
        blog = Blog.objects.get(uid=request.GET.get('pk'))
        blog_image_url = blog.image.url
        publisher = User.objects.get(username=blog.publisher)
        comments = Comment.objects.filter(blog=request.GET.get('pk')).values()
        recent_blogs = Blog.objects.all().order_by('publish_date')[:5][::-1]
        # print(comments)
        tags = blog.tags.split(",")

        context = {
            'uid': blog.uid,
            'title': blog.title,
            'image': blog_image_url,
            'desc': blog.desc,
            'publish_date': blog.publish_date,
            'publisher': f"{publisher.first_name} {publisher.last_name}",
            'tags': tags,
            'comments': list(comments),
            'recent_blogs': list(recent_blogs),
        }
    except:
        context = {'info' : '404 - Blog not Found'}

    return render(request, 'app/blog-details.html', context=context)


#### API ####

class getServices(viewsets.GenericViewSet, 
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin):

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class getTestimonials(viewsets.GenericViewSet, 
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin):

    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


class getFaqs(viewsets.GenericViewSet, 
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin):

    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
    

class getBlogs(viewsets.GenericViewSet, 
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin):

    queryset = Blog.objects.all().order_by('publish_date')
    serializer_class = BlogSerializer


class getComments(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin):

    queryset = Comment.objects.all().order_by('publish_date')
    serializer_class = CommentSerializer

   
class postMessage(viewsets.GenericViewSet, 
                mixins.CreateModelMixin):

    queryset = ContactForm.objects.all()    
    serializer_class = ContactFormSerializer

    def get_ip_location(self, http_header):

        ip = ''
        x_forwarded_for = http_header.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = http_header.get('REMOTE_ADDR')

        # database = IP2Location.IP2Location(os.path.join("data", "IPV4-COUNTRY.BIN"))

        # rec = database.get_all(ip)

        return ip


    def send_email(self, form_data, http_header):

        try:
            remote_ip = self.get_ip_location(http_header)
        except:
            remote_ip = 'Can not get IP'
    
        form_message = form_data['message']
        subject = form_data['subject']
        
        try:
            email = form_data['email']
        except:
            email = 'INVALID EMAIL'
            
        message = f'Sender: {email} \nIP Address: {remote_ip} \nMessage: \n {form_message}'

        send_mail(subject, 
            message, 
            from_email=settings.EMAIL_HOST_USER, 
            recipient_list=[settings.ADMIN_EMAIL], 
            fail_silently=False) 

    
    def create(self, request, *arg, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers=self.get_success_headers(serializer.data)
        
        self.send_email(request.data, request.headers)
        print('email sent')

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        serializer.save()
