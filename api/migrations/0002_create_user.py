# Generated by Django 5.1.3 on 2024-11-29 05:21

from django.db import migrations
import bcrypt

# Function for creating a new registration in the users table
def create_default_user(apps, schema_editor):
    # Loads the model that is going to be used
    User = apps.get_model('api', 'User')

    # We create a registration with the next data (hashed password)
    if not User.objects.filter(username='demo_user').exists():
        User.objects.create(
            username='demo_user',
            email='demo@example.com',
            password= bcrypt.hashpw('demo_password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        )

# Migration class that Django uses
class Migration(migrations.Migration):
    # Is necessary to add the last migration to make it work
    dependencies = [
        ('api', '0001_initial'),
    ]

    # We use the function to create a default user
    operations = [
        migrations.RunPython(create_default_user),
    ]