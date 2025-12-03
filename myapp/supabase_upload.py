from supabase import create_client
from django.conf import settings
import uuid
import os

def upload_to_supabase(file):
  supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

  file_ext = file.name.split('.')[-1]
  file_name = f"{uuid.uuid4()}.{file_ext}"
  path = f"avatars/{file_name}"

  supabase.storage.form_(settings.SUPABASE_BUCKET).upload(
    path,
    file.read(),
    file_options={"content-type": file.content_type}
  )

  public_url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(path)
  return public_url
