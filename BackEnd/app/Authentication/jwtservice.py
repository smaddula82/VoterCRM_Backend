from jwt import PyJWT
from time import time
from typing import Union
from app.Models.Logins import *


class JWTService:
    expires_in_seconds = 2592000
    signing_algorithm = "HS256"

    def __init__(self, signing_key: str, expires_in_seconds: int = 2592000):
        self.signing_key = signing_key
        self.expires_in_seconds = expires_in_seconds

    def generate(
        self, data: dict, expires_in_secods: int = expires_in_seconds
    ) -> Union[str, None]:
        try:
            instance = PyJWT()
            curr_unix_epoch = int(time())
            data["iat"] = curr_unix_epoch

            if isinstance(expires_in_secods, int):
                data["exp"] = curr_unix_epoch + expires_in_secods

            token = instance.encode(
                payload=data, key=self.signing_key, algorithm=self.signing_algorithm
            )

            if type(token) == bytes:
                token = token.decode("utf-8")

            return token
        except:
            return None

    def get_payload(self, token: str):
        try:
            instance = PyJWT()
            payload = instance.decode(
                jwt=token, key=self.signing_key, algorithms=[self.signing_algorithm]
            )
            return payload
        except:
            return None

    def is_valid(self, token: str, verify_time: bool = True) -> bool:
        try:
            login = Logins.query.filter_by(Token=token).first()
            if not login or login.Status == "LoggedOut":
                print("User not logged in")
                return False
            payload = self.get_payload(token)
            if payload is None:
                return False
            if verify_time and "exp" in payload and payload["exp"] < int(time()):
                return False
            return True
        except:
            return False
