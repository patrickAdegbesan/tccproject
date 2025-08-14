from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tccwebsite.models import Instructor, Course, Testimonial, BlogPost

class Command(BaseCommand):
    help = 'Load sample courses and instructors'

    def handle(self, *args, **options):
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@tccacademy.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        else:
            admin_user = User.objects.get(username='admin')

        # Create sample instructors
        instructors_data = [
            {
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'email': 'sarah@tccacademy.com',
                'bio': 'Full-stack developer with 10+ years of experience in web development and teaching.',
                'specialization': 'Web Development',
                'experience_years': 10
            },
            {
                'first_name': 'Michael',
                'last_name': 'Chen',
                'email': 'michael@tccacademy.com',
                'bio': 'Data scientist and machine learning expert with extensive industry experience.',
                'specialization': 'Data Science & AI',
                'experience_years': 8
            },
            {
                'first_name': 'Emily',
                'last_name': 'Rodriguez',
                'email': 'emily@tccacademy.com',
                'bio': 'Mobile app developer specializing in iOS and Android development.',
                'specialization': 'Mobile Development',
                'experience_years': 7
            }
        ]

        instructors = []
        for instructor_data in instructors_data:
            user, created = User.objects.get_or_create(
                username=instructor_data['first_name'].lower() + '_' + instructor_data['last_name'].lower(),
                defaults={
                    'email': instructor_data['email'],
                    'first_name': instructor_data['first_name'],
                    'last_name': instructor_data['last_name']
                }
            )
            
            instructor, created = Instructor.objects.get_or_create(
                user=user,
                defaults={
                    'bio': instructor_data['bio'],
                    'specialization': instructor_data['specialization'],
                    'experience_years': instructor_data['experience_years']
                }
            )
            instructors.append(instructor)
            if created:
                self.stdout.write(f'Created instructor: {instructor}')

        # Create sample courses
        courses_data = [
            {
                'title': 'Python Programming Fundamentals',
                'description': 'Learn Python programming from scratch with hands-on projects and real-world applications.',
                'difficulty': 'beginner',
                'duration': '8 weeks',
                'price': 150000.00,  # ₦150,000
                'instructor': instructors[0],
                'is_featured': True
            },
            {
                'title': 'Full-Stack Web Development',
                'description': 'Master HTML, CSS, JavaScript, React, and Node.js to become a full-stack developer.',
                'difficulty': 'intermediate',
                'duration': '16 weeks',
                'price': 300000.00,  # ₦300,000
                'instructor': instructors[0],
                'is_featured': True
            },
            {
                'title': 'Data Science with Python',
                'description': 'Explore data analysis, visualization, and machine learning using Python and popular libraries.',
                'difficulty': 'intermediate',
                'duration': '12 weeks',
                'price': 250000.00,  # ₦250,000
                'instructor': instructors[1],
                'is_featured': True
            },
            {
                'title': 'Mobile App Development',
                'description': 'Build native mobile applications for iOS and Android using modern frameworks.',
                'difficulty': 'intermediate',
                'duration': '14 weeks',
                'price': 280000.00,  # ₦280,000
                'instructor': instructors[2],
                'is_featured': False
            },
            {
                'title': 'Advanced JavaScript & React',
                'description': 'Master advanced JavaScript concepts and build complex React applications.',
                'difficulty': 'advanced',
                'duration': '10 weeks',
                'price': 200000.00,  # ₦200,000
                'instructor': instructors[0],
                'is_featured': False
            },
            {
                'title': 'Machine Learning & AI',
                'description': 'Deep dive into machine learning algorithms and artificial intelligence concepts.',
                'difficulty': 'advanced',
                'duration': '16 weeks',
                'price': 350000.00,  # ₦350,000
                'instructor': instructors[1],
                'is_featured': False
            }
        ]

        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults=course_data
            )
            if created:
                self.stdout.write(f'Created course: {course}')

        # Create sample testimonials
        testimonials_data = [
            {
                'student_name': 'Alex Thompson',
                'content': 'The Python course was amazing! The instructor explained everything clearly and the projects were very practical.',
                'rating': 5,
                'is_featured': True,
                'course': Course.objects.get(title='Python Programming Fundamentals')
            },
            {
                'student_name': 'Maria Garcia',
                'content': 'Great full-stack course. I landed my dream job as a web developer after completing this program.',
                'rating': 5,
                'is_featured': True,
                'course': Course.objects.get(title='Full-Stack Web Development')
            },
            {
                'student_name': 'David Kim',
                'content': 'The data science course opened up new career opportunities for me. Highly recommended!',
                'rating': 4,
                'is_featured': True,
                'course': Course.objects.get(title='Data Science with Python')
            }
        ]

        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                student_name=testimonial_data['student_name'],
                defaults=testimonial_data
            )
            if created:
                self.stdout.write(f'Created testimonial: {testimonial}')

        # Create sample blog posts
        blog_posts_data = [
            {
                'title': '5 Programming Languages to Learn in 2025',
                'slug': '5-programming-languages-2025',
                'content': '''<p>The technology landscape is constantly evolving, and choosing the right programming language to learn can significantly impact your career prospects. Here are the top 5 programming languages you should consider learning in 2025:</p>

<h3>1. Python</h3>
<p>Python continues to dominate in data science, AI, and web development. Its simple syntax and powerful libraries make it perfect for beginners and experts alike.</p>

<h3>2. JavaScript</h3>
<p>Essential for web development, JavaScript now powers both frontend and backend applications with frameworks like React, Vue.js, and Node.js.</p>

<h3>3. Rust</h3>
<p>Gaining popularity for system programming and performance-critical applications. Companies like Microsoft and Meta are investing heavily in Rust.</p>

<h3>4. Go</h3>
<p>Google's Go language is perfect for cloud computing and microservices architecture. Its simplicity and performance make it a great choice for modern applications.</p>

<h3>5. TypeScript</h3>
<p>As JavaScript applications grow in complexity, TypeScript provides the type safety and tooling needed for large-scale development.</p>''',
                'excerpt': 'Discover the top 5 programming languages that will be in high demand in 2025 and why you should consider learning them.',
                'is_published': True,
                'author': admin_user
            },
            {
                'title': 'How to Build Your First Web Application',
                'slug': 'build-first-web-application',
                'content': '''<p>Building your first web application can seem daunting, but with the right approach, it's an exciting journey. Here's a step-by-step guide to get you started:</p>

<h3>Step 1: Choose Your Technology Stack</h3>
<p>For beginners, we recommend starting with HTML, CSS, and JavaScript for the frontend, and Python with Django or Flask for the backend.</p>

<h3>Step 2: Plan Your Application</h3>
<p>Start with a simple project like a to-do list or personal portfolio. Define the features you want to implement.</p>

<h3>Step 3: Set Up Your Development Environment</h3>
<p>Install a code editor like VS Code, set up version control with Git, and create your project structure.</p>

<h3>Step 4: Build the Frontend</h3>
<p>Create the user interface using HTML and CSS. Add interactivity with JavaScript.</p>

<h3>Step 5: Develop the Backend</h3>
<p>Create your server-side logic, set up a database, and create APIs to connect your frontend and backend.</p>''',
                'excerpt': 'A comprehensive guide for beginners on building their first web application from scratch.',
                'is_published': True,
                'author': admin_user
            }
        ]

        for blog_data in blog_posts_data:
            blog_post, created = BlogPost.objects.get_or_create(
                slug=blog_data['slug'],
                defaults=blog_data
            )
            if created:
                self.stdout.write(f'Created blog post: {blog_post}')

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data!'))