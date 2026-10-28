import express from "express";
import cors from "cors";

const app = express();
// ruleid: ts-express-open-cors-on-loopback-server
app.use(cors());
app.use(express.json());
app.get("/memory", (_req, res) => res.json({ facts: [] }));
app.listen(7700, "127.0.0.1");

const app2 = express();
// ruleid: ts-express-open-cors-on-loopback-server
app2.use(cors({ origin: true, credentials: true }));
const server = app2.listen(7701, "localhost", () => {});

const app3 = express();
// ok: ts-express-open-cors-on-loopback-server
app3.use(cors({ origin: ["http://127.0.0.1:5173"] }));
app3.listen(7702, "127.0.0.1");

const app4 = express();
// ok: ts-express-open-cors-on-loopback-server
app4.use(cors());
app4.listen(8080, "0.0.0.0");
