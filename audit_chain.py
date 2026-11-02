"""A tamper-evident audit log for AI agent decisions, in ~80 lines.

Every entry stores the SHA-256 hash of the entry before it. Edit or delete any entry and
verification fails at exactly that point. Standard library only.

Usage:
  python audit_chain.py demo            # writes a log, verifies, forges an entry, verifies again
  python audit_chain.py verify FILE [HEAD_HASH]
"""
import hashlib
import json
import sys

GENESIS = "0" * 64


def entry_hash(body, prev):
    payload = json.dumps(body, sort_keys=True, separators=(",", ":")) + prev
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def append(log, body):
    prev = log[-1]["hash"] if log else GENESIS
    log.append({"seq": len(log) + 1, "body": body, "prev": prev, "hash": entry_hash(body, prev)})
    return log[-1]["hash"]


def verify(log, head=None):
    """Return (ok, message). Pass the head hash you stored elsewhere to catch a deleted tail."""
    prev = GENESIS
    for i, e in enumerate(log):
        if e["seq"] != i + 1:
            return False, f"entry {i + 1}: sequence gap (an entry was removed)"
        if e["prev"] != prev:
            return False, f"entry {e['seq']}: does not link to the entry before it"
        if entry_hash(e["body"], e["prev"]) != e["hash"]:
            return False, f"entry {e['seq']}: content was changed after it was written"
        prev = e["hash"]
    if head and prev != head:
        return False, "log ends early: the stored head hash does not match (tail deleted)"
    return True, f"{len(log)} entries verified"


def save(log, path):
    with open(path, "w", encoding="utf-8") as fh:
        for e in log:
            fh.write(json.dumps(e) + "\n")


def load(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def demo():
    log = []
    calls = [("schema_browse", "allow"), ("recipient_sample", "allow_masked"),
             ("query_run DELETE", "block"), ("delivery_send BF-HR-01", "needs_approval"),
             ("delivery_send BF-HR-01", "approved by: ops.lead")]
    head = None
    for tool, decision in calls:
        head = append(log, {"tool": tool, "decision": decision})
    print("1. Clean log:           ", verify(log, head)[1])

    forged = json.loads(json.dumps(log))
    forged[2]["body"]["decision"] = "allow"
    print("2. 'block' -> 'allow':  ", verify(forged, head)[1])

    rehashed = json.loads(json.dumps(forged))
    rehashed[2]["hash"] = entry_hash(rehashed[2]["body"], rehashed[2]["prev"])
    print("3. Forged + re-hashed:  ", verify(rehashed, head)[1])

    removed = [e for e in log if e["seq"] != 3]
    print("4. Entry 3 deleted:     ", verify(removed, head)[1])

    truncated = log[:-1]
    print("5. Last entry deleted:  ", verify(truncated)[1], "  <- without a stored head hash")
    print("   ...with head hash:   ", verify(truncated, head)[1])


if __name__ == "__main__":
    args = sys.argv[1:] or ["demo"]
    if args[0] == "demo":
        demo()
    elif args[0] == "verify":
        ok, msg = verify(load(args[1]), args[2] if len(args) > 2 else None)
        print(msg)
        sys.exit(0 if ok else 1)
