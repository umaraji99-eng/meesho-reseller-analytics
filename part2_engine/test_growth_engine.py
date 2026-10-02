from part2_engine.growth_engine import (
    mom_growth,
    is_flagged,
    validate_feed,
)


def test_ethnic_wear_april_to_may():
    # GIVEN
    previous = 104520.77
    current = 185107.61

    # WHEN
    mom = mom_growth(previous, current)
    result = is_flagged(mom)

    # THEN
    assert mom == 77.1
    assert result == "flagged"


def test_beauty_may_to_june():
    # GIVEN
    previous = 35542.11
    current = 37559.07

    # WHEN
    mom = mom_growth(previous, current)
    result = is_flagged(mom)

    # THEN
    assert mom == 5.67
    assert result == "not_flagged"


def test_exact_threshold_boundary():
    # GIVEN
    previous = 100000
    current = 108000

    # WHEN
    mom = mom_growth(previous, current)
    result = is_flagged(mom)

    # THEN
    assert mom == 8.0
    assert result == "escalate_exact_boundary"


def test_corrupted_feed():
    # GIVEN
    csv_path = "part2_engine/fixtures/corrupted_feed.csv"

    # WHEN
    valid, errors = validate_feed(csv_path)

    # THEN
    assert valid is False

    assert errors == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]

def test_valid_monthly_category_revenue_feed():
    # GIVEN
    csv_path = "part2_engine/fixtures/monthly_category_revenue.csv"

    # WHEN
    valid, errors = validate_feed(csv_path)

    # THEN
    assert valid is True
    assert errors == []

def test_may_vs_april_mom_table():
    # GIVEN
    cases = [
        (104520.77, 185107.61, 77.1, "flagged"),
        # Add the actual April/May values for the remaining categories here
    ]

    # WHEN / THEN
    for previous, current, expected_mom, expected_flag in cases:
        mom = mom_growth(previous, current)
        result = is_flagged(mom)

        assert mom == expected_mom
        assert result == expected_flag
