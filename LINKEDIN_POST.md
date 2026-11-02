Safe to Send · Ep 06 — The audit log that catches a lie

I edited one line of my agent's audit log, from "block" to "allow". Verification failed at exactly that entry.

Then I tried to cover it up by recalculating the hash. It failed one entry later, because the next entry still pointed at the original.

Then I found the gap most demos skip: delete the *last* entry, and a hash chain verifies perfectly. The remaining links are all still valid.

The fix costs nothing: store the latest hash somewhere the agent can't write. Verify against that, and a cut-short log fails too.

80 lines of Python, five attacks, one lesson: tamper-evident only works if the evidence lives in two places.

Repo: https://github.com/sghatge/safe-to-send-06-audit-chain

#SafeToSend #Audit #AIGovernance
