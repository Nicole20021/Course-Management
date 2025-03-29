from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default_admin(sender, **kwargs):
    from .models import User

    if not User.objects.filter(username="admin").exists():
        user = User.objects.save(
            {
                'username':"admin",
                'first_name':"Nicole",
                'last_name':"Almoughrabi",
                'password':"admin",
            }
        )
        user.role = 'admin'
        user.save()
        
        print("✅ Default admin user created!")
        
class CoursemanagementappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CourseManagementApp'
    
    def ready(self):
        post_migrate.connect(create_default_admin, sender=self)