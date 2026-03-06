"""Simple email address validator using only the Python standard library.

No regex, no third-party dependencies. Validates structural rules based on
RFC 5321 length limits and basic format expectations.
"""

__all__ = ["validate_email"]


def validate_email(email: str) -> bool:
    """Check whether an email address is structurally valid.

    Args:
        email: The email address string to validate.

    Returns:
        True if the address passes all checks, False otherwise.

    Checks performed:
        - Non-empty string
        - No spaces anywhere
        - Exactly one @ symbol
        - Non-empty local part (before @) and domain (after @)
        - Local part <= 64 characters
        - Domain <= 253 characters
        - Total length <= 254 characters
        - Domain contains at least one dot
        - No empty labels in the domain (e.g. ``example..com``)
        - Domain does not start or end with a dot/hyphen
    """
    if not isinstance(email, str) or not email:
        return False

    if " " in email:
        return False

    if len(email) > 254:
        return False

    if email.count("@") != 1:
        return False

    local_part, domain = email.split("@")

    if not local_part or len(local_part) > 64:
        return False

    if not domain or len(domain) > 253:
        return False

    if "." not in domain:
        return False

    labels = domain.split(".")
    for label in labels:
        if not label:
            return False
        if label.startswith("-") or label.endswith("-"):
            return False

    return True


if __name__ == "__main__":
    test_cases: list[tuple[str, bool]] = [
        ("user@example.com", True),
        ("alice.bob+tag@sub.domain.org", True),
        ("x@a.b", True),
        ("", False),
        ("missing-at-sign.com", False),
        ("two@@signs.com", False),
        ("@no-local.com", False),
        ("no-domain@", False),
        ("no-dot@localhost", False),
        ("has space@example.com", False),
        ("user@.leading-dot.com", False),
        ("user@trailing-dot.com.", False),
        ("user@double..dot.com", False),
        ("user@-leading-hyphen.com", False),
        ("a" * 65 + "@example.com", False),
        ("user@" + "a" * 254 + ".com", False),
    ]

    for email, expected in test_cases:
        result = validate_email(email)
        status = "PASS" if result == expected else "FAIL"
        display = email if len(email) <= 40 else email[:37] + "..."
        print(f"  {status}  validate_email({display!r}) -> {result}")
