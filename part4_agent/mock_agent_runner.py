import csv
import json
import sys
from pathlib import Path

from part2_engine.growth_engine import (
    validate_feed,
    mom_growth,
    is_flagged,
)


TOP_N = 3


def load_rows(csv_path: str) -> list[dict]:
    """Load monthly revenue rows from a CSV file."""
    with open(csv_path, "r", newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def get_month(rows: list[dict]) -> str:
    """Return the month stored in the CSV."""
    return rows[0]["month"]


def fill_prompt_template(
    category: str,
    previous_revenue: float,
    current_revenue: float,
    mom_pct: float,
    month: str,
    prev_month: str,
) -> str:
    """
    Fill the Part 3 prompt-pack template.

    Only verified Part 1 / Part 2 values are used.
    No message is sent; this only creates a draft.
    """
    return (
        f"Context: {category} revenue is being compared from "
        f"{prev_month} to {month}.\n"
        f"Insight: Fact — {category} revenue changed by "
        f"{mom_pct}% MoM from {prev_month} to {month}.\n"
        f"Implication: Action — The regional manager should review "
        f"{category} performance between {prev_month} and {month} "
        f"before taking corrective action."
    )


def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    """
    Run the mock monitoring agent.

    Drafts messages only. Nothing is automatically sent.
    """

    # ---------------------------------------------------------
    # 1. Validate the previous-month feed.
    # ---------------------------------------------------------
    previous_valid, previous_errors = validate_feed(previous_month_csv)

    # ---------------------------------------------------------
    # 2. Validate the current-month feed.
    # ---------------------------------------------------------
    current_valid, current_errors = validate_feed(current_month_csv)

    validation_errors = previous_errors + current_errors

    # ---------------------------------------------------------
    # Hard Stop if either feed is invalid.
    # ---------------------------------------------------------
    if not previous_valid or not current_valid:
        result = {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": validation_errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

        print(json.dumps(result, indent=2))
        return result

    # ---------------------------------------------------------
    # 3. Load validated feeds.
    # ---------------------------------------------------------
    previous_rows = load_rows(previous_month_csv)
    current_rows = load_rows(current_month_csv)

    previous_month = get_month(previous_rows)

    previous_by_category = {
        row["category"]: float(row["revenue"])
        for row in previous_rows
    }

    current_by_category = {
        row["category"]: float(row["revenue"])
        for row in current_rows
    }

    # ---------------------------------------------------------
    # 4. Calculate MoM and classify every category.
    # ---------------------------------------------------------
    flagged = []
    escalated_categories = []

    for category, current_revenue in current_by_category.items():

        if category not in previous_by_category:
            continue

        previous_revenue = previous_by_category[category]

        mom_pct = mom_growth(
            previous_revenue,
            current_revenue
        )

        status = is_flagged(mom_pct)

        item = {
            "category": category,
            "mom_pct": mom_pct,
            "previous_revenue": previous_revenue,
            "current_revenue": current_revenue,
        }

        if status == "flagged":
            flagged.append(item)

        elif status == "escalate_exact_boundary":
            escalated_categories.append(category)

    # ---------------------------------------------------------
    # 5. Sort flagged categories by absolute MoM descending.
    # ---------------------------------------------------------
    flagged.sort(
        key=lambda item: abs(item["mom_pct"]),
        reverse=True
    )

    # ---------------------------------------------------------
    # 6. Draft messages for top 3 only.
    # ---------------------------------------------------------
    drafted_categories = flagged[:TOP_N]

    for item in drafted_categories:
        item["drafted"] = True

        item["message"] = fill_prompt_template(
            category=item["category"],
            previous_revenue=item["previous_revenue"],
            current_revenue=item["current_revenue"],
            mom_pct=item["mom_pct"],
            month=month,
            prev_month=previous_month,
        )

    # ---------------------------------------------------------
    # 7. Suppress remaining flagged categories.
    # ---------------------------------------------------------
    suppressed_categories = [
        item["category"]
        for item in flagged[TOP_N:]
    ]

    # ---------------------------------------------------------
    # 8. Emit structured JSON.
    # ---------------------------------------------------------
    result = {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": drafted_categories,
        "suppressed_categories": suppressed_categories,
        "escalated_categories": escalated_categories,
        "action_taken": "drafted_and_held_for_approval",
    }

    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print(
            "Usage: python part4_agent/mock_agent_runner.py "
            "<run_month> <previous_month_csv> <current_month_csv>"
        )
        sys.exit(1)

    run(
        month=sys.argv[1],
        previous_month_csv=sys.argv[2],
        current_month_csv=sys.argv[3],
    )