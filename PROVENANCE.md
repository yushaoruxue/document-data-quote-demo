# Provenance and Evidence Boundary

## Classification

**Synthetic / internal proof. Not a client case.**

The public-facing demo was created as a compact evidence surface from already-demonstrated internal capability patterns. It intentionally does not expose private delivery infrastructure.

## Earlier internal evidence reused

### DTR-01 Dataset-to-Report capability test — 2026-09-12

Internal synthetic validation previously demonstrated:

- 131 raw order rows;
- 101 clean rows;
- 30 excluded rows;
- explicit warnings / exception handling;
- V1 and V2 rule changes;
- reconciliation PASS;
- **20/20** automated assertions PASS;
- versioned rule configuration and rerunnable processing.

That evidence was synthetic and was never a stranger-client case.

### SPIKE-03 Power Query / Excel consolidation — 2026-09-12

Internal Windows validation previously demonstrated:

- Microsoft Excel Power Query execution;
- multi-file normalization / append;
- explicit invalid and duplicate exception output;
- Refresh All after adding a new file;
- Refresh All after a client-style rule change;
- independent oracle reconciliation;
- workbook outputs updating after refresh.

That evidence was also synthetic and does not establish client production history.

## What is new in this proof

This repository surface narrows those patterns to a buyer-readable responsibility:

```text
structured RFQ rows
→ exact approved-catalogue match
→ quote draft
+ unsafe rows → human-review queue
→ acceptance checks
```

The included six-row sample and its outputs were reproduced independently for this showcase. The showcase does **not** claim that the earlier DTR-01 or Power Query package was a client RFQ project.

## Private material intentionally excluded

Not published here:

- personal execution infrastructure;
- browser/session/authentication internals;
- credentials or tokens;
- reusable private orchestration;
- unrelated private repositories;
- student/client/private source material.
