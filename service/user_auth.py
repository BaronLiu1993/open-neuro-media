from service.supabase_client import get_supabase_client


def login_user(email: str, password: str) -> tuple:
    sb = get_supabase_client()
    res = sb.auth.sign_in_with_password({"email": email.lower().strip(), "password": password})
    return (res.session.access_token, res.session.refresh_token, res.user.id)


def register_user(email: str, password: str) -> tuple:
    sb = get_supabase_client()
    res = sb.auth.sign_up({"email": email.lower().strip(), "password": password})
    doc = {"user_id": res.user.id, "email": email.lower().strip()}
    sb.table("users").insert(doc).execute()
    return (res.session.access_token, res.session.refresh_token, res.user.id)
