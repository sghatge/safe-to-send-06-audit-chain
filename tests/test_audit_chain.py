import json
import unittest

from audit_chain import append, verify


def build(n=5):
    log, head = [], None
    for i in range(n):
        head = append(log, {"i": i})
    return log, head


class AuditChainTest(unittest.TestCase):
    def test_clean(self):
        log, head = build()
        self.assertTrue(verify(log, head)[0])

    def test_edit_detected(self):
        log, head = build()
        log[1]["body"]["i"] = 99
        ok, msg = verify(log, head)
        self.assertFalse(ok)
        self.assertIn("entry 2", msg)

    def test_rehash_detected_at_next_link(self):
        from audit_chain import entry_hash
        log, head = build()
        log[1]["body"]["i"] = 99
        log[1]["hash"] = entry_hash(log[1]["body"], log[1]["prev"])
        ok, msg = verify(log, head)
        self.assertFalse(ok)
        self.assertIn("entry 3", msg)

    def test_middle_deletion_detected(self):
        log, head = build()
        del log[2]
        self.assertFalse(verify(log, head)[0])

    def test_tail_deletion_needs_head(self):
        log, head = build()
        self.assertTrue(verify(log[:-1])[0])
        self.assertFalse(verify(log[:-1], head)[0])


if __name__ == "__main__":
    unittest.main()
