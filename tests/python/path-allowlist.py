import os
from pathlib import Path

import fitz
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pdf-reader")
ALLOWED = [Path(p).resolve() for p in os.environ.get("MCP_PDF_ALLOWED_DIRS", "").split(os.pathsep) if p]


def ensure_allowed(path: Path) -> Path:
    real = path.resolve()
    if not any(real.is_relative_to(root) for root in ALLOWED):
        raise PermissionError(f"Access denied: {path} is outside the configured allowed directories")
    return real


@mcp.tool()
def read_pdf(path: str) -> str:
    # ruleid: python-mcp-tool-path-without-allowlist
    doc = fitz.open(path)
    return "".join(page.get_text() for page in doc)


@mcp.tool()
async def read_text(file_path: str) -> str:
    p = Path(file_path).expanduser()
    # ruleid: python-mcp-tool-path-without-allowlist
    return p.read_text()


@mcp.tool()
def read_pdf_checked(path: str) -> str:
    safe = ensure_allowed(Path(path))
    # ok: python-mcp-tool-path-without-allowlist
    doc = fitz.open(safe)
    return "".join(page.get_text() for page in doc)


@mcp.tool()
def list_dir(directory: str) -> list[str]:
    real = Path(directory).resolve()
    real.relative_to(ALLOWED[0])
    # ok: python-mcp-tool-path-without-allowlist
    return [e.name for e in real.iterdir()]


def not_a_tool(path: str) -> str:
    # ok: python-mcp-tool-path-without-allowlist
    with open(path) as fh:
        return fh.read()
