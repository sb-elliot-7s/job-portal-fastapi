from settings import get_settings

TOKEN_DATA: dict = {
    'secret_key': get_settings().secret_key,
    'algorithm': get_settings().algorithm,
}
ACCESS_TOKEN_DATA: dict = {
    **TOKEN_DATA,
    'exp_time': get_settings().access_token_expire_minutes
}

REFRESH_TOKEN_DATA: dict = {
    **TOKEN_DATA,
    'exp_time': get_settings().refresh_token_expire_minutes
}
