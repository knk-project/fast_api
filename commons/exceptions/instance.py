from typing import Any, Optional, Dict

from fastapi import HTTPException
from starlette.status import (
    HTTP_409_CONFLICT, HTTP_404_NOT_FOUND
)


class UniqueException(HTTPException):
    def __init__(
            self,
            status_code: int = HTTP_409_CONFLICT,
            key: Any = None,
            value: Any = None,
            detail: Any = None,
            headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if not detail:
            if key or value:
                detail = f'Instance with `{key}: {value}` already exists.'
            else:
                detail = f'Instance already exists.'

        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers


class InstanceNotFound(HTTPException):
    def __init__(
            self,
            status_code: int = HTTP_404_NOT_FOUND,
            detail: Any = None,
            headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if not detail:
            detail = f'Not found.'

        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers
