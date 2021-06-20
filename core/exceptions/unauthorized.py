from fastapi import HTTPException
from starlette import status


class Unauthorized(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Could not validate credentials'
    headers = {"WWW-Authenticate": "Bearer"}

    def __init__(self, detail: str = None):
        if detail:
            self.detail = detail

        super().__init__(status_code=self.status_code, detail=self.detail,
                         headers=self.headers)
