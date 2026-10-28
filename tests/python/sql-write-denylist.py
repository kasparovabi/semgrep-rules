import re

# ruleid: python-sql-write-keyword-denylist-without-into
WRITE_KEYWORDS = {"INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP", "TRUNCATE"}

# ruleid: python-sql-write-keyword-denylist-without-into
FORBIDDEN = ("insert", "update", "delete")

# ok: python-sql-write-keyword-denylist-without-into
PATCHED = ["INSERT", "UPDATE", "DELETE", "INTO", "OUTFILE", "DUMPFILE"]

# ok: python-sql-write-keyword-denylist-without-into
READS = ["SELECT", "SHOW", "EXPLAIN"]


def is_read_only(sql: str) -> bool:
    words = set(re.findall(r"[A-Za-z_]+", sql.upper()))
    return sql.strip().upper().startswith("SELECT") and not (words & WRITE_KEYWORDS)
