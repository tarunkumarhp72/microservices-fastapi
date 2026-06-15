from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


# ── Custom Exception Classes ──────────────────────────────────────────

class BaseAppException(Exception):
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class NotFoundException(BaseAppException):
  
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail=detail, status_code=404)


class UnauthorizedException(BaseAppException):
    
    def __init__(self, detail: str = "Authentication required"):
        super().__init__(detail=detail, status_code=401)


class ForbiddenException(BaseAppException):
   
    def __init__(self, detail: str = "You do not have permission"):
        super().__init__(detail=detail, status_code=403)


class ConflictException(BaseAppException):
    
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(detail=detail, status_code=409)


class BadRequestException(BaseAppException):
  
    def __init__(self, detail: str = "Bad request"):
        super().__init__(detail=detail, status_code=400)


class ServiceUnavailableException(BaseAppException):
    
    def __init__(self, detail: str = "Service temporarily unavailable"):
        super().__init__(detail=detail, status_code=503)


# ── Standard Error Response ───────────────────────────────────────────

def _error_response(status_code: int, error: str, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": error,
            "detail": detail,
            "status_code": status_code,
        }
    )


# ── Global Exception Handlers ───────────

def register_exception_handlers(app: FastAPI):
   

    @app.exception_handler(BaseAppException)
    async def app_exception_handler(request: Request, exc: BaseAppException):
        names = {400: "Bad Request", 401: "Unauthorized", 403: "Forbidden",
                 404: "Not Found", 409: "Conflict", 503: "Service Unavailable"}
        return _error_response(exc.status_code, names.get(exc.status_code, "Error"), exc.detail)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return _error_response(exc.status_code, "HTTP Error", str(exc.detail))

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        for err in exc.errors():
            field = " → ".join(str(loc) for loc in err["loc"])
            errors.append(f"{field}: {err['msg']}")
        return _error_response(422, "Validation Error", "; ".join(errors))

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return _error_response(500, "Internal Server Error",str(exc))