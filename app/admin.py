from django.contrib import admin
from app.models import Service, Testimonial, Faq, Blog, Comment, ContactForm

class ServiceAdmin(admin.ModelAdmin):
    pass


class TestimonialAdmin(admin.ModelAdmin):
    pass


class FaqAdmin(admin.ModelAdmin):
    pass


class BlogAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass

class ContactFormAdmin(admin.ModelAdmin):
    pass



admin.site.register(Service, ServiceAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ContactForm, ContactFormAdmin)



