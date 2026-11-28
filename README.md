<div align="center">

<img src="assets/portfolio/repo-card.svg" width="520" alt="safe-to-send-06-audit-chain bespoke project visual">

**SAFE TO SEND · GOVERNED AI ENGINEERING SERIES · SAFE TO SEND 06 AUDIT CHAIN**

[GitHub Profile](https://github.com/sghatge) · [Portfolio](https://sghatge.github.io/adobe-campaign-v8-governance/)

</div>

---

# safe-to-send-06 · Audit Chain

![Safe to Send, Episode 06](docs/episode.png)

**Safe to Send · Episode 06** — a 28-day learn-in-public series on governing AI in CRM operations.

> If agents act in your CRM, the record of what they did must be harder to change than the action itself.

## The real-world scenario

After an incident, someone opens the agent's log and changes one line from `block` to `allow`. Now the story says the agent was allowed to do what it did. With an ordinary log file, nobody can tell.

## Run it

```bash
python audit_chain.py demo
```

## Real example output

```
1. Clean log:            5 entries verified
2. 'block' -> 'allow':   entry 3: content was changed after it was written
3. Forged + re-hashed:   entry 4: does not link to the entry before it
4. Entry 3 deleted:      entry 3: sequence gap (an entry was removed)
5. Last entry deleted:   4 entries verified   <- without a stored head hash
   ...with head hash:    log ends early: the stored head hash does not match (tail deleted)
```

## The lesson most hash-chain demos skip

Line 5. A hash chain proves nothing is changed *inside* the log. It cannot tell you the log was cut short, because the remaining entries still link perfectly. The fix is cheap: store the latest hash (the "head") somewhere the agent can't write, such as a ticket, a separate system or a daily email, and verify against it.

## Use it

```python
from audit_chain import append, verify
log = []
head = append(log, {"tool": "delivery_send", "decision": "needs_approval"})
ok, message = verify(log, head)
```

## Where this fits

[ACC Agent Gate](https://github.com/sghatge/acc-agent-gate) writes every decision, including blocks, to a log like this one.

Independent project, not affiliated with Adobe. Synthetic data only. MIT · [Sangram Ghatge](https://www.linkedin.com/in/sangram-g-2369705b) · #SafeToSend


---

## Portfolio integration & safe use

This repository is part of the **Safe to Send** 28-episode engineering series on governed AI for CRM and marketing operations.

- [Series index and episode map](https://github.com/sghatge/safe-to-send-21-series-map)
- [Complete portfolio](https://github.com/sghatge/sghatge)
- [OPSFORGE Build Lab](https://sghatge.streamlit.app/) — portfolio overview; this repository remains independently usable without the Build Lab.

**Safe-use boundary:** use the supplied examples and synthetic data for evaluation. Review the implementation, dependencies and tests before adapting it. Do not connect it to a production CRM, customer dataset or activation endpoint without a separate security, privacy and change-control review. No production integration or deployment is implied by this repository.
