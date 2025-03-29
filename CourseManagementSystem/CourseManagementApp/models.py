import re
from django.contrib.auth.hashers import check_password, make_password
from django.db import models

class UserManager(models.Manager):
    def save(self, fields):
        return self.create(
            username = fields['username'],
            first_name = fields['first_name'],
            last_name = fields['last_name'],
            phone = fields.get('phone', None),
            email = fields.get('email', None),
            password = make_password(fields['password'])  # Hash the password before saving
            )
   
    def select(self, username):
        try:
            return self.get(username=username)
        except:
            return None
        
    def validate_login(self, fields):
        errors = {}
        # Check if both username and password are provided
        if not fields.get('username'):
            errors['username'] = "Username is required."
        if not fields.get('password'):
            errors['password'] = "Password is required."
        # If any field is missing, return errors immediately
        if errors:
            return errors
        # Check if the user exists
        try:
            user = self.get(username=fields['username'])
        except:
            errors['username'] = "User not found."
            return errors
        # Verify password (if using Django's password hashing)
        if not check_password(fields['password'], user.password):
            errors['password'] = "Incorrect password."

        return errors
    
    def validate_signup(self, fields):
        errors = {}
        # Required Fields Validation
        required_fields = ['username', 'first_name', 'last_name', 'password']
        for field in required_fields:
            if not fields.get(field):
                errors[field] = f"{field.replace('_', ' ').title()} is required."

        # Username uniqueness
        if 'username' in fields:
            if ' ' in fields['username']:
                errors['username'] = "Username has space!"
            if User.objects.filter(username=fields['username']).exists():
                errors['username'] = "Username already taken."

        # Email format and uniqueness
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        email = fields.get('email', '')
        if email != '': # The field is not required
            if not re.match(email_regex, fields['email']):
                errors['email'] = "Invalid email format."
            elif User.objects.filter(email=fields['email']).exists():
                errors['email'] = "Email is already registered."

        # Phone number validation
        phone_regex = r'^\+?\d{10,15}$'  # optional + and 10-15 digits
        phone = fields.get('phone', '') 
        if phone != '': # The field is not required
            if not re.match(phone_regex, fields['phone']):
                errors['phone'] = "Invalid phone number."
            elif User.objects.filter(phone=fields['phone']).exists():
                errors['phone'] = "Phone number already in use."

        # Password strength validation
        password = fields.get('password', '')
        if len(password) < 8:
            errors['password'] = "Password must be at least 8 characters long."
        elif not any(char.isdigit() for char in password):
            errors['password'] = "Password must contain at least one digit."
        elif not any(char.isupper() for char in password):
            errors['password'] = "Password must contain at least one uppercase letter."
        elif not any(char.islower() for char in password):
            errors['password'] = "Password must contain at least one lowercase letter."
        elif not any(char in "!@#$%^&*()_+" for char in password):
            errors['password'] = "Password must contain at least one special character."

        if 'password2' not in fields or fields['password2'] != fields.get('password',''):
            errors['confirm'] = "Passwords does not match."
            
        return errors
    
# Custom User Model
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    email = models.CharField(max_length=255, null=True, unique=True)
    password = models.CharField(max_length=50)
    
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True)  # Stores last login time
    
    role = models.CharField(max_length=10, default= "student", choices=[('admin', 'admin'),('student', 'student')])
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.username} ({self.role})"

# Course Model
class Course(models.Model):
    name = models.CharField(max_length=255)
    field = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    credits = models.IntegerField()
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    sale = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    description = models.TextField()

    def final_cost(self):
        return self.cost - (self.cost * self.sale/100)

    def __str__(self):
        return self.name

# Enrollment Model
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.name}"


