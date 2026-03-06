"""Comprehensive test suite for email_validator.validate_email.

Covers:
    - Valid emails (standard, subdomains, plus addressing, long local parts)
    - Invalid emails (structural failures for every validation branch)
    - Edge cases (boundary lengths, minimum valid, special characters)
    - Type errors (non-string input)

Uses pytest.mark.parametrize throughout for clarity and easy extension.
"""

import pytest

from email_validator import validate_email


# ---------------------------------------------------------------------------
# Valid emails
# ---------------------------------------------------------------------------

class TestValidEmails:
    """Emails that should be accepted by validate_email."""

    @pytest.mark.parametrize(
        "email",
        [
            pytest.param("user@example.com", id="standard-address"),
            pytest.param("alice@example.co.uk", id="two-level-tld"),
            pytest.param("bob@mail.sub.domain.org", id="deep-subdomain"),
        ],
    )
    def test_standard_addresses(self, email: str) -> None:
        assert validate_email(email) is True

    @pytest.mark.parametrize(
        "email",
        [
            pytest.param("user+tag@example.com", id="plus-addressing"),
            pytest.param("user+billing+2024@example.com", id="multiple-plus-signs"),
            pytest.param("first.last+tag@example.com", id="dots-and-plus"),
        ],
    )
    def test_plus_addressing(self, email: str) -> None:
        assert validate_email(email) is True

    @pytest.mark.parametrize(
        "email",
        [
            pytest.param("a.b.c.d.e@example.com", id="multiple-dots-in-local"),
            pytest.param("first.last@example.com", id="single-dot-in-local"),
        ],
    )
    def test_dots_in_local_part(self, email: str) -> None:
        assert validate_email(email) is True

    @pytest.mark.parametrize(
        "email",
        [
            pytest.param("user_name@example.com", id="underscore"),
            pytest.param("user-name@example.com", id="hyphen"),
            pytest.param("user!def@example.com", id="exclamation"),
            pytest.param("user#box@example.com", id="hash"),
            pytest.param("user%data@example.com", id="percent"),
            pytest.param("user&info@example.com", id="ampersand"),
            pytest.param("user'quote@example.com", id="apostrophe"),
            pytest.param("user*star@example.com", id="asterisk"),
            pytest.param("user/slash@example.com", id="slash"),
            pytest.param("user=equals@example.com", id="equals"),
            pytest.param("user?query@example.com", id="question-mark"),
            pytest.param("user^hat@example.com", id="caret"),
            pytest.param("user`tick@example.com", id="backtick"),
            pytest.param("user{brace@example.com", id="left-brace"),
            pytest.param("user|pipe@example.com", id="pipe"),
            pytest.param("user}brace@example.com", id="right-brace"),
            pytest.param("user~tilde@example.com", id="tilde"),
        ],
    )
    def test_special_characters_in_local_part(self, email: str) -> None:
        """The validator does not restrict local-part character set beyond spaces."""
        assert validate_email(email) is True

    @pytest.mark.parametrize(
        "email",
        [
            pytest.param("x@a.b", id="minimum-viable-email"),
            pytest.param("a@b.c", id="single-char-each-part"),
        ],
    )
    def test_minimum_valid_email(self, email: str) -> None:
        assert validate_email(email) is True

    def test_subdomain_with_hyphens(self) -> None:
        assert validate_email("user@my-domain.example.com") is True

    def test_numeric_domain_labels(self) -> None:
        assert validate_email("user@123.456.com") is True

    def test_numeric_local_part(self) -> None:
        assert validate_email("12345@example.com") is True


# ---------------------------------------------------------------------------
# Invalid emails -- structural failures
# ---------------------------------------------------------------------------

class TestInvalidNoAtSign:
    """Emails with zero or more than one @ symbol."""

    @pytest.mark.parametrize(
        "email",
        [
            pytest.param("plainaddress", id="no-at-at-all"),
            pytest.param("missing-at-sign.com", id="looks-like-domain-only"),
            pytest.param("@@@", id="three-at-signs"),
            pytest.param("user@@example.com", id="double-at"),
            pytest.param("user@name@example.com", id="at-in-local-and-domain"),
        ],
    )
    def test_wrong_number_of_at_signs(self, email: str) -> None:
        assert validate_email(email) is False


class TestInvalidSpaces:
    """Emails containing whitespace."""

    @pytest.mark.parametrize(
        "email",
        [
            pytest.param("has space@example.com", id="space-in-local"),
            pytest.param("user@exam ple.com", id="space-in-domain"),
            pytest.param(" user@example.com", id="leading-space"),
            pytest.param("user@example.com ", id="trailing-space"),
            pytest.param("us er@exa mple.com", id="spaces-in-both-parts"),
        ],
    )
    def test_spaces_rejected(self, email: str) -> None:
        assert validate_email(email) is False


class TestInvalidEmptyParts:
    """Emails where local part or domain is empty."""

    @pytest.mark.parametrize(
        "email",
        [
            pytest.param("@example.com", id="empty-local-part"),
            pytest.param("user@", id="empty-domain"),
            pytest.param("@", id="just-at-sign"),
        ],
    )
    def test_empty_local_or_domain(self, email: str) -> None:
        assert validate_email(email) is False


class TestInvalidDomainFormat:
    """Emails with malformed domain parts."""

    @pytest.mark.parametrize(
        "email",
        [
            pytest.param("user@localhost", id="no-dot-in-domain"),
            pytest.param("user@example", id="single-label-domain"),
        ],
    )
    def test_domain_missing_dot(self, email: str) -> None:
        assert validate_email(email) is False

    @pytest.mark.parametrize(
        "email",
        [
            pytest.param("user@.example.com", id="leading-dot"),
            pytest.param("user@example.com.", id="trailing-dot"),
            pytest.param("user@.com", id="leading-dot-short"),
        ],
    )
    def test_domain_leading_or_trailing_dot(self, email: str) -> None:
        """Leading/trailing dots produce an empty label after split."""
        assert validate_email(email) is False

    @pytest.mark.parametrize(
        "email",
        [
            pytest.param("user@example..com", id="double-dot"),
            pytest.param("user@a...b.com", id="triple-dot"),
        ],
    )
    def test_domain_consecutive_dots(self, email: str) -> None:
        assert validate_email(email) is False

    @pytest.mark.parametrize(
        "email",
        [
            pytest.param("user@-example.com", id="leading-hyphen-first-label"),
            pytest.param("user@example-.com", id="trailing-hyphen-first-label"),
            pytest.param("user@example.-com", id="leading-hyphen-second-label"),
            pytest.param("user@example.com-", id="trailing-hyphen-last-label"),
            pytest.param("user@-a.com", id="leading-hyphen-short-label"),
            pytest.param("user@a-.com", id="trailing-hyphen-short-label"),
        ],
    )
    def test_domain_label_hyphen_boundaries(self, email: str) -> None:
        assert validate_email(email) is False

    def test_hyphen_in_middle_of_label_is_valid(self) -> None:
        """Hyphens are only invalid at label start/end, not in the middle."""
        assert validate_email("user@my-domain.com") is True


# ---------------------------------------------------------------------------
# Invalid emails -- length violations
# ---------------------------------------------------------------------------

class TestInvalidLengths:
    """Emails exceeding RFC 5321 length limits."""

    def test_local_part_too_long_65_chars(self) -> None:
        local = "a" * 65
        assert validate_email(f"{local}@example.com") is False

    def test_local_part_at_limit_64_chars(self) -> None:
        local = "a" * 64
        assert validate_email(f"{local}@example.com") is True

    def test_domain_too_long_254_chars(self) -> None:
        # Build a domain that exceeds 253 characters
        domain = "a" * 254 + ".com"
        assert validate_email(f"user@{domain}") is False

    def test_domain_253_chars_rejected_by_total_length(self) -> None:
        # A 253-char domain is within the domain limit (<=253), but the
        # shortest possible email with it is 1 + 1 + 253 = 255 total, which
        # exceeds the 254 total-length cap. So it must still be rejected.
        domain = ".".join(["a" * 61] * 4) + "." + "a" * 4 + "x"
        assert len(domain) == 253
        email = f"u@{domain}"
        assert len(email) == 255
        assert validate_email(email) is False

    def test_domain_252_chars_is_valid(self) -> None:
        # 252-char domain with 1-char local = 254 total, which is the max.
        domain = "a" * 125 + "." + "a" * 126  # 125 + 1 + 126 = 252
        assert len(domain) == 252
        email = f"u@{domain}"
        assert len(email) == 254
        assert validate_email(email) is True

    def test_total_length_exactly_254_is_valid(self) -> None:
        # local@domain = 254 total.  local = 1, @ = 1, domain = 252
        # domain must have a dot and be <= 253
        local = "u"
        # domain: 252 chars with a dot
        domain = "a" * 125 + "." + "a" * 126  # 125 + 1 + 126 = 252
        email = f"{local}@{domain}"
        assert len(email) == 254
        assert validate_email(email) is True

    def test_total_length_255_is_invalid(self) -> None:
        local = "uu"
        domain = "a" * 125 + "." + "a" * 126  # 252
        email = f"{local}@{domain}"
        assert len(email) == 255
        assert validate_email(email) is False


# ---------------------------------------------------------------------------
# Empty and blank inputs
# ---------------------------------------------------------------------------

class TestEmptyAndBlankInputs:
    """Empty strings, whitespace-only strings, and similar degenerate input."""

    def test_empty_string(self) -> None:
        assert validate_email("") is False

    def test_whitespace_only(self) -> None:
        assert validate_email("   ") is False

    def test_tab_only(self) -> None:
        assert validate_email("\t") is False


# ---------------------------------------------------------------------------
# Type errors -- non-string input
# ---------------------------------------------------------------------------

class TestTypeErrors:
    """Non-string inputs should return False, not raise."""

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(None, id="none"),
            pytest.param(42, id="integer"),
            pytest.param(3.14, id="float"),
            pytest.param(True, id="bool-true"),
            pytest.param(False, id="bool-false"),
            pytest.param([], id="empty-list"),
            pytest.param({}, id="empty-dict"),
            pytest.param(("user", "example.com"), id="tuple"),
            pytest.param(b"user@example.com", id="bytes"),
        ],
    )
    def test_non_string_returns_false(self, value: object) -> None:
        assert validate_email(value) is False  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Boundary conditions and unusual-but-valid/invalid patterns."""

    def test_single_character_local_and_minimal_domain(self) -> None:
        assert validate_email("a@b.c") is True

    def test_at_sign_only(self) -> None:
        assert validate_email("@") is False

    def test_dot_only(self) -> None:
        assert validate_email(".") is False

    def test_local_part_is_all_dots(self) -> None:
        # The validator does not restrict dots in local part
        assert validate_email("...@example.com") is True

    def test_domain_single_char_labels(self) -> None:
        assert validate_email("user@a.b") is True

    def test_very_long_valid_email_at_254_boundary(self) -> None:
        # 64 char local + @ + 189 char domain = 254
        local = "a" * 64
        # domain: need 189 chars with at least one dot, no empty labels
        domain = "b" * 94 + "." + "c" * 94  # 94 + 1 + 94 = 189
        email = f"{local}@{domain}"
        assert len(email) == 254
        assert len(local) == 64
        assert len(domain) == 189
        assert validate_email(email) is True

    def test_local_part_with_consecutive_dots(self) -> None:
        # Validator does not check local part for consecutive dots
        assert validate_email("user..name@example.com") is True

    def test_local_part_starting_with_dot(self) -> None:
        assert validate_email(".user@example.com") is True

    def test_local_part_ending_with_dot(self) -> None:
        assert validate_email("user.@example.com") is True

    def test_plus_at_start_of_local(self) -> None:
        assert validate_email("+user@example.com") is True

    def test_plus_at_end_of_local(self) -> None:
        assert validate_email("user+@example.com") is True

    def test_domain_with_many_labels(self) -> None:
        assert validate_email("user@a.b.c.d.e.f.g.h") is True

    def test_hyphen_in_middle_of_every_label(self) -> None:
        assert validate_email("user@a-1.b-2.c-3") is True

    def test_all_numeric_tld(self) -> None:
        assert validate_email("user@example.123") is True
