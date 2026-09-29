from __future__ import annotations

import csv
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "samples" / "rfq_rows.csv"
CATALOGUE = ROOT / "samples" / "approved_catalogue.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)


def money(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


catalogue = {}
with CATALOGUE.open(newline="", encoding="utf-8") as handle:
    for row in csv.DictReader(handle):
        catalogue[row["item_code"].strip()] = row

quote_rows = []
review_rows = []

with INPUT.open(newline="", encoding="utf-8") as handle:
    for row in csv.DictReader(handle):
        code = row["item_code"].strip()

        try:
            quantity = Decimal(row["quantity"].strip())
        except Exception:
            quantity = Decimal("-1")

        reason = None
        if not code:
            reason = "MISSING_CODE"
        elif quantity <= 0:
            reason = "INVALID_QUANTITY"
        elif code not in catalogue:
            reason = "UNKNOWN_CODE"

        if reason:
            review_rows.append(
                {
                    **row,
                    "review_reason": reason,
                    "decision": "HUMAN_REVIEW_REQUIRED",
                }
            )
            continue

        approved = catalogue[code]
        unit_price = Decimal(approved["unit_price_usd"])
        line_total = unit_price * quantity

        quote_rows.append(
            {
                "line_id": row["line_id"],
                "item_code": code,
                "requested_description": row["description"],
                "approved_description": approved["approved_description"],
                "quantity": row["quantity"],
                "unit": row["unit"],
                "unit_price_usd": money(unit_price),
                "line_total_usd": money(line_total),
                "status": "QUOTED_FROM_APPROVED_CATALOGUE",
            }
        )

quote_fields = [
    "line_id",
    "item_code",
    "requested_description",
    "approved_description",
    "quantity",
    "unit",
    "unit_price_usd",
    "line_total_usd",
    "status",
]
review_fields = [
    "line_id",
    "item_code",
    "description",
    "quantity",
    "unit",
    "review_reason",
    "decision",
]

with (OUT / "quote_draft.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=quote_fields)
    writer.writeheader()
    writer.writerows(quote_rows)

with (OUT / "review_queue.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=review_fields)
    writer.writeheader()
    writer.writerows(review_rows)

quote_total = sum(Decimal(row["line_total_usd"]) for row in quote_rows)
summary = {
    "input_rows": len(quote_rows) + len(review_rows),
    "quoted_rows": len(quote_rows),
    "review_rows": len(review_rows),
    "quote_total_usd": money(quote_total),
    "unauthorized_price_sources": 0,
    "auto_substitutions": 0,
}

(OUT / "run_summary.json").write_text(
    json.dumps(summary, indent=2),
    encoding="utf-8",
)

print(summary)
