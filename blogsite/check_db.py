import os
import django
from django.db import connections
from django.db.utils import OperationalError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogsite.settings")
django.setup()

def check_db():
    db_conn = connections['default']
    try:
        db_conn.cursor()
        print("SUCCESS: Database connection established!")
        return True
    except OperationalError as e:
        print(f"FAILURE: Could not connect to database. Error: {e}")
        return False
    except Exception as e:
         print(f"FAILURE: An error occurred: {e}")
         return False

if __name__ == "__main__":
    check_db()
