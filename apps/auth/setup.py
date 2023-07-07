from fastapi_users.authentication.strategy import JWTStrategy
from fastapi_users.authentication import AuthenticationBackend, CookieTransport
from db.cred import SECRET

cookie_transport = CookieTransport(cookie_max_age=None, cookie_name="security_")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=2592000)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

