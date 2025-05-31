from functools import wraps
from fastapi import HTTPException
from starlette.responses import JSONResponse


class CustomBaseException(Exception):
    def __init__(self, status, message, detail):            
        super().__init__(message)
            
        self.status = status
        self.error = message
        self.detail = detail


def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except CustomBaseException as e:
            return JSONResponse(
                status_code=e.status,
                content={
                    "error": e.error,
                    "detail": e.detail,
                }
            )
        
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        
        except ValueError as e:
            return JSONResponse(status_code=400, content={"detail": str(e)})
        
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": "Internal Server Error1", "detail": str(e)})
        
    return wrapper
