from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.core.cache import cache
from .models import Course, Instructor, Testimonial, BlogPost, Contact, StudentProfile, Enrollment, Newsletter
from .forms import ContactForm, CustomUserCreationForm, StudentProfileForm, UserUpdateForm, NewsletterForm

def home(request):
    """Homepage with featured courses and testimonials"""
    featured_courses = Course.objects.filter(is_featured=True)[:3]
    testimonials = Testimonial.objects.filter(is_featured=True)[:3]
    recent_posts = BlogPost.objects.filter(is_published=True)[:3]
    
    context = {
        'featured_courses': featured_courses,
        'testimonials': testimonials,
        'recent_posts': recent_posts,
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'home.html', context)

def courses(request):
    """Courses listing page with filtering"""
    courses = Course.objects.all().order_by('-created_at')
    difficulty_filter = request.GET.get('difficulty')
    search_query = request.GET.get('search')
    
    if difficulty_filter:
        courses = courses.filter(difficulty=difficulty_filter)
    
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(instructor__user__first_name__icontains=search_query) |
            Q(instructor__user__last_name__icontains=search_query)
        )
    
    paginator = Paginator(courses, 6)  # Show 6 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'difficulty_filter': difficulty_filter,
        'search_query': search_query,
        'difficulty_choices': Course.DIFFICULTY_CHOICES,
    }
    return render(request, 'courses.html', context)

def course_detail(request, pk):
    """Individual course detail page"""
    course = get_object_or_404(Course, pk=pk)
    related_courses = Course.objects.filter(
        difficulty=course.difficulty
    ).exclude(pk=pk)[:3]
    
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            student=request.user, course=course
        ).exists()
    
    context = {
        'course': course,
        'related_courses': related_courses,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'course_detail.html', context)

@login_required
def enroll_course(request, pk):
    """Enroll user in a course"""
    course = get_object_or_404(Course, pk=pk)
    
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course,
        defaults={'status': 'active'}
    )
    
    if created:
        messages.success(request, f'Successfully enrolled in {course.title}!')
    else:
        messages.info(request, f'You are already enrolled in {course.title}.')
    
    return redirect('course_detail', pk=pk)

def about(request):
    """About page with instructors"""
    instructors = Instructor.objects.all()
    
    context = {
        'instructors': instructors,
    }
    return render(request, 'about.html', context)

def admissions(request):
    """Admissions information page"""
    return render(request, 'admissions.html')

def blog(request):
    """Blog listing page"""
    posts = BlogPost.objects.filter(is_published=True)
    
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'blog.html', context)

def blog_detail(request, slug):
    """Individual blog post detail"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    recent_posts = BlogPost.objects.filter(
        is_published=True
    ).exclude(slug=slug)[:3]
    
    context = {
        'post': post,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog_detail.html', context)

def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'contact.html', context)

def _get_client_ip(request):
    """Best-effort client IP extractor for rate limiting."""
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


def register(request):
    """User registration"""
    if request.method == 'POST':
        # Simple rate limit: max 5 registrations attempts per hour per IP
        ip = _get_client_ip(request)
        rl_key = f"register_attempts:{ip}"
        attempts = cache.get(rl_key, 0)
        if attempts >= 5:
            messages.error(request, 'Too many registration attempts. Please try again later.')
            return redirect('register')

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create student profile
            StudentProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to The Coding School.')
            return redirect('profile')
        else:
            cache.set(rl_key, attempts + 1, 3600)  # 1 hour TTL
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    """User profile page"""
    try:
        student_profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        student_profile = StudentProfile.objects.create(user=request.user)
    
    enrollments = Enrollment.objects.filter(student=request.user)
    
    context = {
        'student_profile': student_profile,
        'enrollments': enrollments,
    }
    return render(request, 'registration/profile.html', context)

@login_required
def edit_profile(request):
    """Edit user profile"""
    try:
        student_profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        student_profile = StudentProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = StudentProfileForm(request.POST, request.FILES, instance=student_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = StudentProfileForm(instance=student_profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'registration/edit_profile.html', context)

@require_POST
@csrf_protect
def newsletter_subscribe(request):
    """AJAX newsletter subscription with CSRF protection and POST-only."""
    form = NewsletterForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            return JsonResponse({'success': True, 'message': 'Successfully subscribed to newsletter!'})
        except Exception:
            return JsonResponse({'success': False, 'message': 'You are already subscribed to our newsletter.'})
    else:
        return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('profile')

    # Basic brute-force protection using cache per IP
    def dispatch(self, request, *args, **kwargs):
        ip = _get_client_ip(request)
        if cache.get(f"login_blocked:{ip}"):
            messages.error(request, 'Too many login attempts. Please try again in 15 minutes.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        request = self.request
        ip = _get_client_ip(request)
        key = f"login_attempts:{ip}"
        attempts = cache.get(key, 0) + 1
        cache.set(key, attempts, 600)  # track for 10 minutes
        if attempts >= 5:
            cache.set(f"login_blocked:{ip}", True, 900)  # block for 15 minutes
        messages.error(request, 'Invalid username or password.')  # generic error
        return super().form_invalid(form)

    def form_valid(self, form):
        # On success, clear any rate-limit flags
        ip = _get_client_ip(self.request)
        cache.delete(f"login_attempts:{ip}")
        cache.delete(f"login_blocked:{ip}")
        return super().form_valid(form)

def custom_logout(request):
    """Custom logout view that handles both GET and POST requests"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')
