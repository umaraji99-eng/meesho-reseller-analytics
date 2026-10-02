import csv


def mom_growth(previous: float, current: float) -> float:
    return round((current - previous) / previous * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    if abs(mom_pct) > threshold:
        return "flagged"
    elif abs(mom_pct) < threshold:
        return "not_flagged"
    else:
        return "escalate_exact_boundary"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    errors = []

    with open(csv_path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for line_number, row in enumerate(reader, start=2):
            row = {
                key.strip(): value.strip() if value is not None else ""
                for key, value in row.items()
            }

            month = row["month"]
            category = row["category"]
            revenue = row["revenue"]

            if not category:
                errors.append(
                    f"line {line_number}: missing category (month={month})"
                )

            if not revenue:
                errors.append(
                    f"line {line_number}: missing revenue (category={category})"
                )
                continue

            try:
                revenue_value = float(revenue)
            except ValueError:
                errors.append(
                    f"line {line_number}: revenue not numeric: {revenue!r}"
                )
                continue

            if revenue_value < 0:
                errors.append(
                    f"line {line_number}: negative revenue ({revenue_value}) "
                    f"for category={category}"
                )

    return (True, []) if len(errors) == 0 else (False, errors)

def test_valid_monthly_category_revenue_feed():
    # GIVEN
    csv_path = "part2_engine/fixtures/monthly_category_revenue.csv"

    # WHEN
    valid, errors = validate_feed(csv_path)

    # THEN
    assert valid is True
    assert errors == []
