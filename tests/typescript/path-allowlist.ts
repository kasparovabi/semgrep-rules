import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import fs from "node:fs/promises";
import path from "node:path";

const server = new McpServer({ name: "pdf-reader", version: "1.0.0" });
const allowedDirs = (process.env.MCP_PDF_ALLOWED_DIRS ?? "").split(path.delimiter).filter(Boolean);

async function assertAllowed(p: string): Promise<string> {
  const real = await fs.realpath(p);
  if (!allowedDirs.some((root) => real === root || real.startsWith(root + path.sep))) {
    throw new Error(`Access denied: path ${p} is outside the configured allowed directories`);
  }
  return real;
}

server.tool("read_pdf", { path: z.string() }, async ({ path: p }) => {
  // ruleid: ts-mcp-tool-path-without-allowlist
  const data = await fs.readFile(p);
  return { content: [{ type: "text", text: data.toString("base64") }] };
});

server.registerTool("read_text", { inputSchema: { file: z.string() } }, async (args) => {
  // ruleid: ts-mcp-tool-path-without-allowlist
  const text = await fs.readFile(path.resolve(args.file), "utf8");
  return { content: [{ type: "text", text }] };
});

server.tool("read_pdf_checked", { path: z.string() }, async ({ path: p }) => {
  const real = await assertAllowed(p);
  // ok: ts-mcp-tool-path-without-allowlist
  const data = await fs.readFile(real);
  return { content: [{ type: "text", text: data.toString("base64") }] };
});

async function cli(p: string) {
  // ok: ts-mcp-tool-path-without-allowlist
  return fs.readFile(p);
}
