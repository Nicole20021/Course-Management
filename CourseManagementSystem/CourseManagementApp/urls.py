from django.urls import path
from . import views


urlpatterns = [
    # registration
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # course
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/add/', views.course_add, name='course_add'),
    path('courses/edit/<int:course_id>/', views.course_edit, name='course_edit'),
    path('courses/delete/<int:course_id>/', views.course_delete, name='course_delete'),
    path('courses/enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('courses/cancel/<int:course_id>/', views.cancel_enrollment, name='cancel_enrollment'),
    # student
    path('students/', views.student_list, name='student_list'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    path('students/<int:student_id>/activation/', views.student_activation, name='student_activation'),
    # admin
    path('reports/', views.reports_view, name='reports'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # 
    path('about/', views.about_view, name='about'),
]