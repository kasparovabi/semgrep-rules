package sqlguard

import "strings"

// The shape before WhoDB 0.134.0.
// ruleid: go-sql-write-keyword-denylist-without-into
var mutatingKeywords = []string{
	"INSERT", "UPDATE", "DELETE", "MERGE", "UPSERT", "REPLACE",
	"CREATE", "ALTER", "DROP", "TRUNCATE", "GRANT", "REVOKE",
}

// ruleid: go-sql-write-keyword-denylist-without-into
var writeVerbs = map[string]bool{"insert": true, "update": true, "delete": true}

// ruleid: go-sql-write-keyword-denylist-without-into
var writeSet = map[string]struct{}{"INSERT": {}, "UPDATE": {}, "DELETE": {}, "DROP": {}}

// ok: go-sql-write-keyword-denylist-without-into
var patchedSet = map[string]struct{}{"INSERT": {}, "UPDATE": {}, "DELETE": {}, "INTO": {}}

// ok: go-sql-write-keyword-denylist-without-into
var patched = []string{"INSERT", "UPDATE", "DELETE", "INTO", "OUTFILE", "DUMPFILE"}

// ok: go-sql-write-keyword-denylist-without-into
var readVerbs = []string{"SELECT", "SHOW", "EXPLAIN", "DESCRIBE"}

func IsMutating(q string) bool {
	upper := strings.ToUpper(q)
	for _, kw := range mutatingKeywords {
		if strings.Contains(upper, kw) {
			return true
		}
	}
	return false
}

// ok: go-sql-write-keyword-denylist-without-into
var buttons = map[string]bool{"insert": true, "append": true, "delete": true}
