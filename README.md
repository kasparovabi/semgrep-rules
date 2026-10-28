# Semgrep rules from published advisories

[Türkçe](README.tr.md)

Semgrep rules for the bug classes behind security advisories I reported and the maintainers published. Each class has a short guide on how to protect your own code. The write-ups for the advisories are in [kasparovabi/security-research](https://github.com/kasparovabi/security-research).

Only published and fixed issues are used here. Reports that are still in private triage do not appear in the rules, the tests or this README.

## Layout

```
rules/<language>/<class>.yaml   rules
tests/<language>/<class>.<ext>  positive (ruleid) and negative (ok) examples for semgrep --test
```

## Usage

Scan a project:

```sh
docker run --rm --network none -v "$PWD":/src semgrep/semgrep \
  semgrep --metrics off --config /path/to/rules /src
```

or with a local install, `semgrep --config rules/ path/to/project`.

Run the tests:

```sh
./test.sh
# same as:
docker run --rm --network none -v "$PWD":/src:ro -w /src semgrep/semgrep \
  semgrep --test --config rules tests
```

The SQL tests use `-- # ruleid:` comments, because `semgrep --test` reads `#` and `//` annotations but not plain `--` comments.

## Rules

| Class | Rule | Languages | Advisory |
|---|---|---|---|
| DNS rebinding, missing Host/Origin check | `go-host-origin-guard-skips-safe-methods` | Go | [GHSA-g57x-rm7r-hf26](https://github.com/devantler-tech/ksail/security/advisories/GHSA-g57x-rm7r-hf26) |
| | `ts-host-origin-guard-skips-safe-methods` | TS/JS | |
| | `ts-mcp-http-transport-without-dns-rebinding-protection` | TS/JS | |
| | `python-mcp-dns-rebinding-protection-disabled` | Python | |
| | `python-loopback-server-without-host-check` (audit) | Python | [GHSA-682p-grrx-wrwg](https://github.com/GuyMannDude/mnemo-cortex/security/advisories/GHSA-682p-grrx-wrwg) |
| CORS on a loopback API | `python-cors-allows-any-origin` | Python | [GHSA-682p-grrx-wrwg](https://github.com/GuyMannDude/mnemo-cortex/security/advisories/GHSA-682p-grrx-wrwg) |
| | `python-cors-origin-regex-matches-anything` | Python | |
| | `python-flask-cors-default-any-origin` | Python | |
| | `ts-express-open-cors-on-loopback-server` | TS/JS | |
| Allowed-directory limit not enforced | `python-mcp-tool-path-without-allowlist` | Python | [GHSA-qr3f-g5wf-225w](https://github.com/SylphxAI/anymd/security/advisories/GHSA-qr3f-g5wf-225w) |
| | `ts-mcp-tool-path-without-allowlist` | TS/JS | |
| Allocation sized by input | `rust-allocation-sized-by-parsed-count` | Rust | [GHSA-p2qw-h8m7-5x69](https://github.com/embedded-society/altium-designer-mcp/security/advisories/GHSA-p2qw-h8m7-5x69) |
| | `rust-grow-loop-driven-by-parsed-index` | Rust | |
| Supabase / Postgres RLS | `postgres-rls-policy-using-true-for-anon` | SQL | [GHSA-8h52-3cfj-cmrw](https://github.com/Kronova-Intelligent-Systems/asset-intel-orchestration-engine/security/advisories/GHSA-8h52-3cfj-cmrw) |
| | `postgres-rls-policy-with-check-true-for-anon` | SQL | |
| | `postgres-rls-disabled` | SQL | |
| SQL write denylist without INTO | `go-sql-write-keyword-denylist-without-into` | Go | [GHSA-pvf2-6h4x-r24j](https://github.com/clidey/whodb/security/advisories/GHSA-pvf2-6h4x-r24j) |
| | `python-sql-write-keyword-denylist-without-into` | Python | |
| | `ts-sql-write-keyword-denylist-without-into` | TS/JS | |
| Modules removed in Python 3.12 / 3.13 | `python313-removed-stdlib-module` | Python | [PEP 594](https://peps.python.org/pep-0594/) |
| | `python312-removed-stdlib-module` | Python | |

## How to protect yourself

### DNS rebinding on local servers

A server bound to 127.0.0.1 is safe from other machines, but the browser on the same machine can still reach it. A page that rebinds its own hostname to 127.0.0.1 is same-origin to the browser, so it can read the responses, and the only thing that gives it away is the `Host` header. Check `Host` against the names you listen on for every request, including GET, and check `Origin` whenever it is present. A random port only slows an attacker down. Test the routes that return secrets or proxy to another system with the user's credentials first. For MCP servers built on the official SDKs, turn on the transport's DNS rebinding protection and set the allowed hosts.

Advisory: [KSail GHSA-g57x-rm7r-hf26](https://github.com/devantler-tech/ksail/security/advisories/GHSA-g57x-rm7r-hf26), write-up [here](https://github.com/kasparovabi/security-research/blob/main/2026-10-ksail-webui-dns-rebinding.md).

### CORS on a loopback API

`allow_origins=["*"]` is reasonable for a public read-only API and a poor default for a local API that holds private data, because any page in the user's browser can then read it. A check on the peer address does not help, since the browser is also a loopback client. Leave the CORS list empty by default and add only the origins that need access. If the API has no authentication, refuse requests whose `Origin` is not on that list and whose `Host` is not a loopback name, because Origin stops cross-site requests and Host stops rebinding.

Advisory: [mnemo-cortex GHSA-682p-grrx-wrwg](https://github.com/GuyMannDude/mnemo-cortex/security/advisories/GHSA-682p-grrx-wrwg), write-up [here](https://github.com/kasparovabi/security-research/blob/main/2026-10-mnemo-cortex-cors-loopback.md).

### Allowed-directory limits that are not enforced

Security settings in the documentation are part of what users rely on, so a flag like `--allow-dir` has to be enforced by the code, and an unknown flag should stop the program instead of being ignored. Resolve every path the model supplies (following symlinks), and refuse it unless it is under one of the allowed roots. Put that check in one function that every tool taking a path calls, and add a test that runs each such tool with a path outside the roots. New tools are where the check gets missed. Test the package that users install, not only the source.

Advisory: [anymd GHSA-qr3f-g5wf-225w](https://github.com/SylphxAI/anymd/security/advisories/GHSA-qr3f-g5wf-225w), write-up [here](https://github.com/kasparovabi/security-research/blob/main/2026-09-anymd-allow-dir-not-implemented.md).

### Allocations sized by input

Never pass a count read from a file or a request straight to `Vec::with_capacity`, `reserve` or `vec![x; n]`. In Rust a failed allocation aborts the process, and `catch_unwind` cannot stop an abort, so one file can end every session on a server. Bound the count by what the remaining input could describe, for example remaining bytes divided by the smallest record size, because a fixed cap per record still adds up when there are many records. Apply the same check to counts that only drive a loop, which hang instead of aborting.

Advisory: [altium-designer-mcp GHSA-p2qw-h8m7-5x69](https://github.com/embedded-society/altium-designer-mcp/security/advisories/GHSA-p2qw-h8m7-5x69), write-up [here](https://github.com/kasparovabi/security-research/blob/main/2026-10-altium-designer-mcp-unbounded-allocation.md).

### Supabase and Postgres row level security

The anon key ships in every client bundle, so RLS policies are what protect the data. Postgres combines permissive policies with OR, so one `USING (true)` policy for `anon` or `PUBLIC` opens the whole table no matter how narrow the other policies are. Look for the broadest permissive policy per role and command, and replay migrations in order to know the final set. Keep personal columns such as email in tables that have no anonymous read path, and remember that a deployed database may have policies that the repository does not show.

Advisory: [asset-intel-orchestration-engine GHSA-8h52-3cfj-cmrw](https://github.com/Kronova-Intelligent-Systems/asset-intel-orchestration-engine/security/advisories/GHSA-8h52-3cfj-cmrw), write-up [here](https://github.com/kasparovabi/security-research/blob/main/2026-09-kronova-profiles-rls.md).

### Deciding "is this SQL read-only" with a keyword denylist

A list of write verbs cannot answer whether a statement writes. `SELECT ... INTO` creates a table in PostgreSQL and `SELECT ... INTO OUTFILE` writes a file on a MySQL server, and each dialect has more. Parse the statement and accept only a small read grammar, and treat anything else as a write that needs approval. Run read-only sessions in a read-only transaction as a second layer, and use a database account without `CREATE` or `FILE` privilege, since that boundary does not depend on parsing.

Advisory: [WhoDB GHSA-pvf2-6h4x-r24j](https://github.com/clidey/whodb/security/advisories/GHSA-pvf2-6h4x-r24j), write-up [here](https://github.com/kasparovabi/security-research/blob/main/2026-09-whodb-select-into.md).

### Modules removed in Python 3.12 and 3.13

Python 3.13 removed the modules listed in PEP 594 (`cgi`, `pipes`, `telnetlib`, `audioop`, `crypt`, `imghdr` and others), and 3.12 removed `asyncore`, `asynchat`, `smtpd`, `imp` and `distutils`. Code that imports them fails at import time, often in scripts that nobody runs until they are needed. Remove unused imports, and replace the rest (`shlex.quote` for `pipes.quote`, `html.escape` for `cgi.escape`, the `audioop-lts` package for `audioop`). When you need to support old and new versions, guard the import with `try/except ImportError`. This class is about compatibility. The fixes merged from this work are listed in the [security-research README](https://github.com/kasparovabi/security-research#merged-fixes-in-other-projects).

## Limits

These rules are heuristics. Some need context that Semgrep cannot see (for example a Host check in another middleware), so treat a finding as a place to look. The taint rules only follow data inside one function. Issues and pull requests with false positives or missed cases are welcome.

## License

MIT, see [LICENSE](LICENSE).
