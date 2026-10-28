import express from "express";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import { randomUUID } from "node:crypto";

// ruleid: ts-mcp-http-transport-without-dns-rebinding-protection
const t1 = new StreamableHTTPServerTransport({ sessionIdGenerator: () => randomUUID() });

// ruleid: ts-mcp-http-transport-without-dns-rebinding-protection
const t2 = new StreamableHTTPServerTransport({
  sessionIdGenerator: undefined,
  enableDnsRebindingProtection: false,
});

// ok: ts-mcp-http-transport-without-dns-rebinding-protection
const t3 = new StreamableHTTPServerTransport({
  sessionIdGenerator: () => randomUUID(),
  enableDnsRebindingProtection: true,
  allowedHosts: ["127.0.0.1:3000", "localhost:3000"],
});

const app = express();
app.get("/sse", (req, res) => {
  // ruleid: ts-mcp-http-transport-without-dns-rebinding-protection
  const sse = new SSEServerTransport("/messages", res);
  // ok: ts-mcp-http-transport-without-dns-rebinding-protection
  const sse2 = new SSEServerTransport("/messages", res, { enableDnsRebindingProtection: true, allowedHosts: ["localhost:3000"] });
});

const UI_ORIGIN = "http://127.0.0.1:4317";

app.use((req, res, next) => {
  // ruleid: ts-host-origin-guard-skips-safe-methods
  if (req.method === "GET" || req.method === "HEAD") {
    return next();
  }
  const host = req.headers.host;
  if ("http://" + host !== UI_ORIGIN) {
    return res.status(403).end();
  }
  next();
});

app.use((req, res, next) => {
  // ok: ts-host-origin-guard-skips-safe-methods
  if (req.method === "OPTIONS") {
    return res.status(204).end();
  }
  const host = req.headers.host;
  if ("http://" + host !== UI_ORIGIN) {
    return res.status(403).end();
  }
  const origin = req.headers.origin;
  if (origin && origin !== UI_ORIGIN) {
    return res.status(403).end();
  }
  next();
});
