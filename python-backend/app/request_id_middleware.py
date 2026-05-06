import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware

from .request_context import request_id_context

logger = logging.getLogger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        incoming_request_id = request.headers.get("X-Request-ID")
        request_id = incoming_request_id if incoming_request_id else str(uuid.uuid4())
        
        token = request_id_context.set(request_id)
        
        start_time = time.perf_counter()
        
        logger.info(
            "HTTP request started",
            extra={
                "event": "request_started",
                "method": request.method,
                "path": request.url.path,
                "request_id": request_id,

            }
        )
        
        try:
            response = await call_next(request)
            
            
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            
            logger.info(
                "HTTP request completed",
                extra={
                    "event": "http_request_completed",
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                }
            )
            
            response.headers["X-Request-ID"] = request_id
            
            return response
        
        except Exception:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            
            logger.exception(
                "HTTP request failed",
                extra={
                    "event": "http_request_failed",
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": duration_ms,
                }
            )
            
            raise
        
        finally:
            request_id_context.reset(token)
        