from django.db import models

class UserManager(models.Manager):
    def save(self, fields):
        return self.create(
            username = fields['username'],
            first_name = fields['first_name'],
            last_name = fields['last_name'],
            email = fields['email'],
            password = fields['password']
            )
    def select(self, username, password):
        try:
            return self.get(username=username, password=password)
        except:
            return None
        
    def validate_login(self, fields):
        return {}
    
    def validate_signup(self, fields):
        return {}

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
    # USERNAME_FIELD = "username"  # Username is used for authentication
    # REQUIRED_FIELDS = ["email", "first_name", "last_name"]  # Extra required fields
    
    # Add related_name to avoid conflict
    # groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    # user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)
    
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


