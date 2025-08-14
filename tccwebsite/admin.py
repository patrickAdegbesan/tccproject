from django.contrib import admin
from .models import Instructor, Course, Testimonial, BlogPost, Contact, StudentProfile, Enrollment, Newsletter

# Register your models here.

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'experience_years']
    list_filter = ['specialization', 'experience_years']
    search_fields = ['user__first_name', 'user__last_name', 'specialization']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'price', 'instructor', 'is_featured', 'created_at']
    list_filter = ['difficulty', 'is_featured', 'instructor', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'price']
    prepopulated_fields = {}

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'course', 'rating', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_featured', 'course', 'created_at']
    search_fields = ['student_name', 'content']
    list_editable = ['is_featured', 'rating']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'created_at']
    list_filter = ['is_published', 'author', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    list_editable = ['is_read']
    readonly_fields = ['created_at']

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'progress_percentage', 'enrollment_date']
    list_filter = ['status', 'enrollment_date', 'course']
    search_fields = ['student__first_name', 'student__last_name', 'course__title']
    list_editable = ['status', 'progress_percentage']

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    list_editable = ['is_active']
