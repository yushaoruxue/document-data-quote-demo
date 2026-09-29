from __future__ import annotations

import csv
import json
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "samples"
OUTPUTS = ROOT / "outputs"

with (SAMPLES / "approved_catalogue.csv").open(newline="", encoding="utf-8") as handle:
    catalogue = {row["item_code"]: row for row in csv.DictReader(handle)}

with (OUTPUTS / "quote_draft.csv").open(newline="", encoding="utf-8") as handle:
    quotes = list(csv.DictReader(handle))

with (OUTPUTS / "review_queue.csv").open(newline="", encoding="utf-8") as handle:
    reviews = list(csv.DictReader(handle))

summary = json.loads((OUTPUTS / "run_summary.json").read_text(encoding="utf-8"))

assert summary["input_rows"] == 6
assert summary["quoted_rows"] == 3
assert summary["review_rows"] == 3
assert Decimal(summary["quote_total_usd"]) == Decimal("176.00")
assert summary["unauthorized_price_sources"] == 0
assert summary["auto_substitutions"] == 0

for row in quotes:
    approved = catalogue[row["item_code"]]
    assert row["unit_price_usd"] == f'{Decimal(approved["unit_price_usd"]):.2f}'
    assert row["status"] == "QUOTED_FROM_APPROVED_CATALOGUE"

reasons = {row["line_id"]: row["review_reason"] for row in reviews}
assert reasons == {
    "4": "UNKNOWN_CODE",
    "5": "MISSING_CODE",
    "6": "INVALID_QUANTITY",
}

# Critical safety boundary: line 5 resembles D-400 by description,
# but the blank item code must not be guessed.
assert all(row["line_id"] != "5" for row in quotes)

print("9/9 acceptance checks PASS")
