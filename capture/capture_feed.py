#!/usr/bin/env python3
"""Second Brain capture feed (read-only).

Prints a bounded digest of recent Hermes sessions for a capture/distil cron job.
Reads the profile's state.db read-only; never writes anything.

Env:
  CAPTURE_HERMES_HOME  profile dir containing state.db (required)
  CAPTURE_VAULT        Obsidian vault root (required; used only to list existing Inbox proposals)
  CAPTURE_HOURS        look-back window in hours (default 26)
  CAPTURE_MAX_CHARS    total digest cap (default 60000)
  CAPTURE_INCLUDE_ONESHOT  set to 1 to include one-shot CLI sessions (rehearsal/demo only)
"""
import os, re, sqlite3, sys, datetime as dt
from pathlib import Path

home = Path(os.environ["CAPTURE_HERMES_HOME"]).expanduser()
vault = Path(os.environ["CAPTURE_VAULT"]).expanduser()
hours = float(os.environ.get("CAPTURE_HOURS", "26"))
cap = int(os.environ.get("CAPTURE_MAX_CHARS", "60000"))
PER_MSG = 700

REDACT = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "<email>"),
    (re.compile(r"\b(?:sk|pk|rk|ghp|gho|xox[abp]|AIza|ya29)[-_A-Za-z0-9]{16,}\b"), "<secret>"),
    (re.compile(r"\b[A-Fa-f0-9]{32,}\b"), "<hex>"),
    (re.compile(r"(?:\+?61|0)4\d{2}[ -]?\d{3}[ -]?\d{3}"), "<phone>"),
    (re.compile(r"(?i)(password|passwd|api[_-]?key|token|secret)\s*[:=]\s*\S+"), r"\1=<redacted>"),
]

def clean(t: str) -> str:
    t = re.sub(r"<memory-context>.*?</memory-context>", "", t or "", flags=re.S)
    t = re.sub(r"\[OUT-OF-BAND USER MESSAGE[^\]]*\]|\[/OUT-OF-BAND USER MESSAGE\]", "", t)
    t = re.sub(r"--- Attached Context ---.*", "[attached context omitted]", t, flags=re.S)
    for rx, rep in REDACT:
        t = rx.sub(rep, t)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:PER_MSG] + ("…" if len(t) > PER_MSG else "")

since = dt.datetime.now().timestamp() - hours * 3600
db = sqlite3.connect(f"file:{home / 'state.db'}?mode=ro", uri=True)
excl = "'cron'" if os.environ.get("CAPTURE_INCLUDE_ONESHOT") == "1" else "'cron','oneshot'"
sessions = db.execute(
    "select id, coalesce(title, display_name, ''), source, started_at from sessions "
    f"where started_at > ? and source not in ({excl}) and parent_session_id is null order by started_at",
    (since,),
).fetchall() if "title" in [c[1] for c in db.execute("pragma table_info(sessions)")] else db.execute(
    "select id, coalesce(display_name, ''), source, started_at from sessions "
    f"where started_at > ? and source not in ({excl}) and parent_session_id is null order by started_at",
    (since,),
).fetchall()

out, used = [], 0
out.append(f"# Session digest: last {hours:g} h, generated {dt.datetime.now():%Y-%m-%d %H:%M}")
out.append(f"Sessions in window: {len(sessions)} (cron, one-shot and subagent sessions excluded)\n")
for sid, title, source, started in sessions:
    rows = db.execute(
        "select role, content from messages where session_id=? and active=1 and role in ('user','assistant') "
        "and content is not null and content != '' order by id",
        (sid,),
    ).fetchall()
    if not rows:
        continue
    block = [f"## Session {sid} · {dt.datetime.fromtimestamp(started):%Y-%m-%d %H:%M} · {source} · {title}"]
    for role, content in rows:
        c = clean(content)
        if c:
            block.append(f"- **{role}**: {c}")
    text = "\n".join(block) + "\n"
    if used + len(text) > cap:
        out.append(f"[digest truncated at {cap} chars; remaining sessions omitted]")
        break
    out.append(text); used += len(text)

inbox = vault / "00 Inbox"
existing = sorted(p.name for p in inbox.glob("Capture proposals *.md")) if inbox.exists() else []
out.append("# Existing capture-proposal files (for de-duplication)")
out.extend(f"- {n}" for n in existing[-14:]) if existing else out.append("- none yet")
print("\n".join(out))
