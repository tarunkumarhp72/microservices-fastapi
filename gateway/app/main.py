import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from app.config import ROUTE_MAP

app = FastAPI(
    title="API Gateway",
    description="Single entry point for all microservices",
    version="1.0.0",
    docs_url="/docs",
)


def get_target_url(path: str) -> str:
    for prefix, service_url in ROUTE_MAP.items():
        if path.startswith(prefix):
            return service_url
    return None


async def proxy_request(request: Request, path: str) -> Response:
    full_path = f"/{path}"
    target_base = get_target_url(full_path)

    if not target_base:
        raise HTTPException(
            status_code=404,
            detail=f"No service found for path: {full_path}"
        )

    # ✅ build target URL with query params
    target_url = f"{target_base}{full_path}"
    if request.query_params:
        target_url += f"?{request.query_params}"

    # ✅ forward headers, remove host
    headers = dict(request.headers)
    headers.pop("host", None)

    body = await request.body()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                timeout=10.0
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=503,
                detail=f"Service unavailable: {target_base}"
            )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail=f"Gateway timeout: {target_base}"
            )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.headers.get("content-type")
    )


# ✅ separate route handlers — no duplicate operation IDs
@app.get("/{path:path}", tags=["Gateway"])
async def proxy_get(request: Request, path: str):
    return await proxy_request(request, path)


@app.post("/{path:path}", tags=["Gateway"])
async def proxy_post(request: Request, path: str):
    return await proxy_request(request, path)


@app.put("/{path:path}", tags=["Gateway"])
async def proxy_put(request: Request, path: str):
    return await proxy_request(request, path)


@app.delete("/{path:path}", tags=["Gateway"])
async def proxy_delete(request: Request, path: str):
    return await proxy_request(request, path)


@app.patch("/{path:path}", tags=["Gateway"])
async def proxy_patch(request: Request, path: str):
    return await proxy_request(request, path)


@app.get("/health", tags=["Health"], include_in_schema=True)
async def health():
    return {"status": "ok", "service": "api-gateway"}