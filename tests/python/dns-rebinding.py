import ipaddress

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

# ruleid: python-mcp-dns-rebinding-protection-disabled
mcp = FastMCP("notes", transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False))

# ok: python-mcp-dns-rebinding-protection-disabled
mcp2 = FastMCP(
    "notes",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=["127.0.0.1:*", "localhost:*"],
        allowed_origins=["http://127.0.0.1:*", "http://localhost:*"],
    ),
)

app = FastAPI()
LOOPBACK = {"127.0.0.1", "::1"}
LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "[::1]"}


@app.middleware("http")
async def loopback_only(request: Request, call_next):
    # ruleid: python-loopback-server-without-host-check
    if request.client.host not in LOOPBACK:
        return JSONResponse({"error": "forbidden"}, status_code=403)
    return await call_next(request)


@app.middleware("http")
async def loopback_and_host(request: Request, call_next):
    # ok: python-loopback-server-without-host-check
    if request.client.host not in LOOPBACK:
        return JSONResponse({"error": "forbidden"}, status_code=403)
    host = request.headers.get("host", "").rsplit(":", 1)[0]
    if host not in LOOPBACK_HOSTS:
        return JSONResponse({"error": "forbidden"}, status_code=403)
    return await call_next(request)
