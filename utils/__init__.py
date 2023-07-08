from starlette.background import BackgroundTask
import typing
import json

class JsonResponse:
    def __init__(
        self,
        message: typing.Any,
        status_code: int = 200
    ) -> None:
        self.message = message
        self.status_code = status_code

        self.response()
    
    def response(self):
        return {"message": self.message, "status": self.status_code}

        