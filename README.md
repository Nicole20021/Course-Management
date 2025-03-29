Course Management System

A Django-based web application for managing courses, students, and enrollments. The system supports user authentication, role-based access, and a user-friendly interface for both admins and students.
📌 Features

    Admin Dashboard: Manage courses and students

    User Roles: Admin & Student with different permissions

    Course Enrollment: Students can enroll and cancel enrollment

    Student Management: Admin can activate/deactivate students

    Authentication: Login, signup, and session-based authentication

    Responsive UI: Bootstrap-integrated design

⚙️ Installation

Follow these steps to set up the project on your local machine.
1️⃣ Clone the Repository

git clone https://github.com/your-username/course-management.git
cd course-management

2️⃣ Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

🛠️ Configuration
4️⃣ Setup Database

Modify settings.py if using a different database (default: SQLite).

Run migrations:

python manage.py makemigrations
python manage.py migrate

5️⃣ Create a Superuser
python manage.py createsuperuser

Enter username, email, and password when prompted.
🚀 Running the Application
6️⃣ Start the Development Server

python manage.py runserver

Visit: http://127.0.0.1:8000/

📂 Project Structure

```
CourseManagementSystem/
│── CourseManagementApp/                # Main Django app
│   ├── migrations/                     # Database migrations
│   ├── static/                         # Static files (CSS, JS)
│   │   ├── css/style.css               # Stylesheet
│   ├── templates/                      # HTML templates
│   │   ├── base.html                   # Main layout
│   │   ├── registration                # Authentication templates      
│   │   │   ├── login.html              # Login page
│   │   │   ├── signup.html             # Signup page
│   │   ├── admin                       # Admin templates
│   │   │   ├── reports.html            # Enrollments Reports 
│   │   │   ├── dashboard.html          # Dashboard
│   │   ├── courses                     # Courses templates
│   │   │   ├── course_list.html        # Courses listing
│   │   │   ├── course_form.html        # Course edit/add pages
│   │   │   ├── course_detail.html      # Course Show page
│   │   ├── student                     # Students templates
│   │   │   ├── student_list.html       # Students listing
│   │   │   ├── student_detail.html     # Student Show page
│   │   ├── about.html                  # About Us page
│   ├── models.py                       # Database models
│   ├── views.py                        # Views (business logic)
│   ├── urls.py                         # URL routing
│── static/                         # Global static files
│── templates/                  # Global templates
│── manage.py                   # Django management script
│── requirements.txt            # Python dependencies
│── README.md                   # Project documentation
```

🔧 Commands Used in This Project
📌 Virtual Environment

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

📌 Django Setup

`django-admin startproject CourseManagementSystem`
`cd CourseManagementSystem`
`python manage.py startapp CourseManagementApp`

📌 Migrations & Database

`python manage.py makemigrations`
`python manage.py migrate`

📌 Superuser & Admin Panel

Did not use `python manage.py createsuperuser` instead creates User with role `admin`
```
python manage.py shell
from CourseManagementApp.models import User
User(username="admin", first_name="Nicole", last_name="Almoughrabi", password="admin", role="admin").save()
```


📌 Running the Server

`python manage.py runserver`

📌 Static Files

`python manage.py collectstatic`

📌 Debugging Static File Issues

`python manage.py findstatic css/style.css`

📌 Troubleshooting & Debugging

`python manage.py shell`

👨‍💻 Contributions

Feel free to fork the repo and submit pull requests.

📜 License

This project is licensed under the MIT License.