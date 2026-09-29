# Acceptance Evidence

> Synthetic demo acceptance. This is not client acceptance.

## Frozen acceptance criteria

The demo passes only when all of the following are true:

1. All 6 input rows are accounted for.
2. Exactly 3 rows are quoted.
3. Exactly 3 rows are sent to human review.
4. Quote total is exactly **$176.00**.
5. Every quoted unit price comes from the approved catalogue row with the same item code.
6. Unknown code `X-999` is not quoted.
7. Blank item code is not auto-matched from description similarity.
8. Zero quantity is not quoted.
9. No automatic substitution or alternate price source is used.

## Current result

`9/9 PASS`

Generated summary:

```json
{
  "input_rows": 6,
  "quoted_rows": 3,
  "review_rows": 3,
  "quote_total_usd": "176.00",
  "unauthorized_price_sources": 0,
  "auto_substitutions": 0
}
```

The checked outputs are committed under `outputs/`.
