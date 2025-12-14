import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "literal_blog.settings")
django.setup()

from django.contrib.auth import get_user_model
import os
from dotenv import load_dotenv

load_dotenv()

User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created.")
else:
    print(f"Superuser '{username}' already exists.")
