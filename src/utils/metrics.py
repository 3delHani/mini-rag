from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Latency', ['method', 'endpoint'])

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        
        start_time = time.perf_counter()
        
        # Process the request
        response = await call_next(request)
        
        # Record metrics after reques is processed
        duration = time.perf_counter() - start_time
        endpoint = request.url.path
        
        REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(duration)
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=response.status_code).inc()
        
        return response
    
def setup_metrics(app: FastAPI):
    """
    setup prometheus metrics middleware and endpoint
    """
    # Add prometheus middleware
    app.add_middleware(PrometheusMiddleware)
        
    @app.get("/dhjk_ljaca", include_in_schema=False)
    def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)