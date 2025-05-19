# dashboard/helpers.py
import os
from django.core.files.storage import default_storage
from django.conf import settings

def delete_user_profile_images(user):
    """
    Deletes all previous profile images for this user.
    Keeps fallback image safe.
    """
    try:
        # Build expected base name like 'profiles/user_1_profile'
        base_name = f"profiles/user_{user.id}_profile"

        # List all files in profiles directory
        _, files = default_storage.listdir('profiles')

        for filename in files:
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                file_path = f"profiles/{filename}"

                # Match against base name (without extension)
                if file_path.startswith(base_name) and 'fallback' not in file_path:
                    if default_storage.exists(file_path):
                        default_storage.delete(file_path)
                        print(f"✅ Deleted old image: {file_path}")
    except Exception as e:
        print(f"❌ Error deleting old images: {e}")