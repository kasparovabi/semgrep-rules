// ruleid: ts-sql-write-keyword-denylist-without-into
const WRITE_KEYWORDS = ["INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP"];

// ruleid: ts-sql-write-keyword-denylist-without-into
const blocked = new Set(["insert", "update", "delete"]);

// ok: ts-sql-write-keyword-denylist-without-into
const patched = ["INSERT", "UPDATE", "DELETE", "INTO", "OUTFILE", "DUMPFILE"];

// ok: ts-sql-write-keyword-denylist-without-into
const reads = ["SELECT", "SHOW", "EXPLAIN"];

export function isReadOnly(sql: string): boolean {
  const upper = sql.trim().toUpperCase();
  return upper.startsWith("SELECT") && !WRITE_KEYWORDS.some((k) => upper.includes(k)) && !blocked.has(upper);
}

// A list of UI actions, not SQL.
// ok: ts-sql-write-keyword-denylist-without-into
const btns = ["insert", "append", "move_up", "move_down", "delete"];
