from fastapi import HTTPException

from starlette import status


class UnauthorizedException(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'You don\'t have permissions.'

    def __init__(self, detail: str = None):
        if detail:
            self.detail = detail

        super().__init__(status_code=self.status_code, detail=self.detail)
