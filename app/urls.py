from django.urls import path, include

from rest_framework.routers import DefaultRouter

from app import views


router = DefaultRouter()

router.register('services', views.getServices, basename='services')
router.register('testimonials', views.getTestimonials, basename='testimonials')
router.register('faqs', views.getFaqs, basename='faqs')
router.register('blogs', views.getBlogs, basename='blogs')
router.register('comments', views.getComments, basename='comments')
router.register('contact', views.postMessage, basename='contact')


app_name = 'app'

urlpatterns = [
    path('', include(router.urls))
]