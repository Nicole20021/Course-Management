from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, User, Enrollment


# Authentication functions
def login(request, user):
    request.session['user'] = {
        'id': user.id,
        'username': user.username,
        'name': f"{user.first_name} {user.last_name}",
        'role': user.role,
        'phone': user.phone
        }
    
def logout(request):
    request.session['user'].clear()
    request.session['user']=None
     
     
# Home view  
def home(request):
    if 'user' in request.session:
        return redirect('course_list')
    return redirect('login')
    
# Authentication Views
# Signup View (For Admin and Student)
def signup_view(request):
    errors = {}
    if request.method == 'POST':
        errors = User.objects.validate_signup(request.POST)
        if len(errors)==0:
            user = User.objects.save(request.POST)
            return redirect('login')
    return render(request, 'registration/signup.html', {'errors': errors, 'fields':request.POST})

# Login View (For Admin and Student)
def login_view(request):
    errors = {}
    if request.method == 'POST':
        errors = User.objects.validate_login(request.POST)
        if len(errors)==0:
            user = User.objects.select(request.POST['username'])
            if user:
                login(request, user)
                return redirect('home')

    return render(request, 'registration/login.html', {'errors': errors, 'fields': request.POST})

# Logout View (For Admin and Student)
def logout_view(request):
    if 'user' in request.session:
        logout(request)
    return redirect('login')

# Course Views
# Course List (For Admin and Student)
def course_list(request):
    if request.session['user']:
        courses = Course.objects.all()
        if request.GET:
            query = request.GET.get('q', '')
            if query:
                courses = Course.objects.filter(name__icontains=query)

        if request.session['user']['role'] == "student":
            student = User.objects.get(id = request.session['user']['id'])
            # Add `is_enrolled` attribute to each course
            for course in courses:
                course.is_enrolled = Enrollment.objects.filter(student=student, course=course).exists()

        return render(request, 'courses/course_list.html', {'courses': courses})

    return redirect('login')

# Course Detail (For Admin and Student)
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

# Course Add (Admin only)
def course_add(request):
    if request.method == 'POST' and request.session['user']['role'] == 'admin':
        name = request.POST['name']
        field = request.POST['field']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        credit = request.POST['credits']
        cost = request.POST['cost']
        sale = request.POST['sale']
        description = request.POST['description']
        Course.objects.create(name=name, field=field, start_date=start_date, end_date=end_date, credits=credit, cost=cost, sale=sale, description=description)
        return redirect('course_list')
    return render(request, 'courses/course_form.html')

# Course Edit (Admin only)
def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST' and request.session['user']['role'] == 'admin':
        course.name = request.POST['name']
        course.field = request.POST['field']
        course.start_date = request.POST['start_date']
        course.credits = request.POST['credits']
        course.cost = request.POST['cost']
        course.sale = request.POST['sale']
        course.description = request.POST['description']
        course.save()
        return redirect('course_list')
    return render(request, 'courses/course_form.html', {'course': course})

# Course Delete (Admin only)
def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.session['user']['role'] == 'admin':
        course.delete()
        return redirect('course_list')
    return redirect('home')

# Enrollment Views
# Enroll Course (Student only)
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if 'user' in request.session and request.session['user']['role'] == 'student':
        student = User.objects.get(id = request.session['user']['id'])
        Enrollment.objects.get_or_create(student=student, course=course)
        return redirect('course_list')
    return redirect('home')

# Cancel Enrollment (Student only)
def cancel_enrollment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = User.objects.get(id = request.session['user']['id'])
    enrollment = Enrollment.objects.filter(student=student, course=course).first()
    if enrollment:
        enrollment.delete()
    return redirect('course_list')

# Student Views
# Student List (Admin Only)
def student_list(request):
    if 'user' in request.session and request.session['user']['role'] == 'admin':
        students = User.objects.filter(role='student')
        if request.GET:
            query = request.GET.get('q', '')
            if query:
                students = User.objects.filter(name__icontains=query, role='student')
        return render(request, 'students/student_list.html', {'students': students})
    
    return redirect('home')

# Student Details (For Admin and Student)
def student_detail(request, student_id):
    student = get_object_or_404(User, id=student_id, role='student')
    enrollments = Enrollment.objects.filter(student=student)
    return render(request, 'students/student_detail.html', {'student': student, 'enrollments': enrollments})

# Student Deactivate (For Admin Only)
def student_activation(request, student_id):
    student = get_object_or_404(User, id=student_id, role='student')
    student.is_active = not student.is_active  # Toggle activation status
    student.save()
    return redirect('student_list')  

# admin
def reports_view(request):
    if request.session['user']['role'] != 'admin':
        return redirect('home')
    courses = Course.objects.prefetch_related('enrollment_set')
    return render(request, 'admin/reports.html', {'courses': courses})

def dashboard_view(request):
    if request.session['user']['role'] != 'admin':
        return redirect('home')
    student_count = User.objects.filter(role='student').count()
    course_count = Course.objects.count()
    return render(request, 'admin/dashboard.html', {'student_count': student_count, 'course_count': course_count})

# about
def about_view(request):
    return render(request, 'about.html')
    