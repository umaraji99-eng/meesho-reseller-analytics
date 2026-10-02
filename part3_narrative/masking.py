def alias_for(reseller_id: str) -> str:
    """
    Convert a reseller ID into an external-facing alias.

    Example:
    RS019 -> ALIAS-19
    RS006 -> ALIAS-06
    """
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(
    text: str,
    reseller_names: list[str]
) -> bool:
    """
    Return False if any raw reseller name appears verbatim in text.
    Return True when no raw reseller name is found.
    """
    return not any(name in text for name in reseller_names)


if __name__ == "__main__":
    # Required alias test
    assert alias_for("RS019") == "ALIAS-19"
    assert alias_for("RS006") == "ALIAS-06"

    reseller_names = [
        "Mumbai Reseller 1",
        "Mumbai Reseller 4",
        "Hyderabad Reseller 6",
        "Lucknow Reseller 6",
        "Jaipur Reseller 5",
    ]

    # Negative-case test:
    # This text still contains a raw reseller name,
    # so the function must return False.
    raw_text = "Top reseller: Mumbai Reseller 1"
    assert assert_no_raw_names_leak(raw_text, reseller_names) is False

    # Final masked narrative:
    masked_text = """
    Mumbai — ALIAS-19
    Mumbai — ALIAS-22
    Hyderabad — ALIAS-12
    Lucknow — ALIAS-06
    Jaipur — ALIAS-05
    """

    # The final narrative must contain no raw reseller names.
    assert assert_no_raw_names_leak(masked_text, reseller_names) is True

    print("All masking tests passed.")