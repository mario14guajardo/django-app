from supabase import create_client
import os
import uuid

def upload_to_supabase(file):
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
    SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET")

    if not SUPABASE_URL or not SUPABASE_KEY or not SUPABASE_BUCKET:
        raise ValueError("Supabase credentials are not set in environment variables.")

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    file_ext = file.name.split('.')[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    path = f"avatars/{file_name}"

    supabase.storage.from_(SUPABASE_BUCKET).upload(
        path,
        file.read(),
        file_options={"content-type": file.content_type}
    )

    public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(path)['public_url']
    return public_url
