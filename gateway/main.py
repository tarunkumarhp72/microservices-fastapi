from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import Response
import httpx

from config import ROUTE_MAP

from shared_lib.middleware import RequestIDMiddleware, ProcessTimeMiddleware
from shared_lib.exceptions import register_exception_handlers
from shared_lib.logger import setup_logger
from shared_lib.rate_limit import RateLimiter

logger = setup_logger(service_name="api-gateway")

gateway_limiter = RateLimiter(limit=100, window_seconds=60)

app = FastAPI(
    title="API Gateway",
    description="Single entry point for all microservices",
    version="1.0.0",
    docs_url="/docs",
)

app.add_middleware(ProcessTimeMiddleware)
app.add_middleware(RequestIDMiddleware)

register_exception_handlers(app)


@app.on_event("startup")
async def startup():
    logger.info("API Gateway started", extra={"port": 8000})


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "service": "api-gateway"}


@app.get("/test")
async def test():
    return {"message": "gateway working"}


def get_target_url(path: str) -> str | None:
    if path in ["/openapi.json", "/docs", "/redoc", "/health", "/test"]:
        return None
    for prefix, service_url in ROUTE_MAP.items():
        if path.startswith(prefix):
            return service_url
    return None


async def proxy_request(request: Request, path: str) -> Response:
    full_path = f"/{path}"
    target_base = get_target_url(full_path)

    if not target_base:
        raise HTTPException(status_code=404, detail=f"No service found for path: {full_path}")

    target_url = f"{target_base}{full_path}"
    if request.query_params:
        target_url += f"?{request.query_params}"

    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(
        f"Proxying {request.method} {full_path}",
        extra={"request_id": request_id, "target": target_url}
    )

    headers = dict(request.headers)
    headers.pop("host", None)
    headers["X-Request-ID"] = request_id  

    body = await request.body()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                timeout=10.0,
            )
    except httpx.ConnectError:
        logger.error(f"Service unavailable: {target_base}", extra={"request_id": request_id})
        raise HTTPException(status_code=503, detail=f"Service unavailable: {target_base}")
    except httpx.TimeoutException:
        logger.warning(f"Gateway timeout: {target_base}", extra={"request_id": request_id})
        raise HTTPException(status_code=504, detail=f"Gateway timeout: {target_base}")

    excluded_headers = {"content-encoding", "content-length", "transfer-encoding", "connection"}
    response_headers = {k: v for k, v in response.headers.items() if k.lower() not in excluded_headers}

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=response_headers,
        media_type=response.headers.get("content-type"),
    )


@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    include_in_schema=False,
)
async def proxy(request: Request, path: str, _=Depends(gateway_limiter)):
    return await proxy_request(request, path)