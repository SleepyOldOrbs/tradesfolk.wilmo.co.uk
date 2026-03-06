# `email_validator` — API Reference

`email_validator` is a single-function Python module that checks whether an email address is structurally valid. It uses no regular expressions and no third-party dependencies — only the Python standard library. Validation is based on RFC 5321 length limits and common format expectations. It does not perform network lookups or full RFC compliance checks.

---

## `validate_email`

```python
def validate_email(email: str) -> bool
```

Returns `True` if `email` passes all structural checks, `False` otherwise.

### Parameters

| Parameter | Type  | Description                        |
|-----------|-------|------------------------------------|
| `email`   | `str` | The email address string to check. |

### Return value

`bool` — `True` if the address is structurally valid, `False` if any check fails.

---

## Validation rules

The function applies these checks in order. The first failure returns `False`.

1. The value must be a non-empty `str` instance.
2. The address must contain no spaces.
3. Total length must not exceed 254 characters.
4. The address must contain exactly one `@` symbol.
5. The local part (before `@`) must be non-empty and at most 64 characters.
6. The domain (after `@`) must be non-empty and at most 253 characters.
7. The domain must contain at least one dot.
8. No domain label (segment between dots) may be empty — rules out `example..com`.
9. No domain label may start or end with a hyphen.

---

## Usage examples

```python
from email_validator import validate_email

# Valid addresses
validate_email("user@example.com")              # True
validate_email("alice.bob+tag@sub.domain.org")  # True
validate_email("x@a.b")                         # True

# Invalid — structural problems
validate_email("")                              # False  (empty string)
validate_email("missing-at-sign.com")           # False  (no @ symbol)
validate_email("two@@signs.com")                # False  (multiple @ symbols)
validate_email("@no-local.com")                 # False  (empty local part)
validate_email("no-domain@")                    # False  (empty domain)
validate_email("no-dot@localhost")              # False  (domain has no dot)
validate_email("has space@example.com")         # False  (space present)
validate_email("user@.leading-dot.com")         # False  (empty domain label)
validate_email("user@trailing-dot.com.")        # False  (empty domain label)
validate_email("user@double..dot.com")          # False  (empty domain label)
validate_email("user@-leading-hyphen.com")      # False  (label starts with hyphen)
validate_email("a" * 65 + "@example.com")       # False  (local part > 64 chars)
validate_email("user@" + "a" * 254 + ".com")    # False  (domain > 253 chars)
```

---

## Limitations

This function performs structural checks only. It does not:

- Verify that the domain exists (no DNS MX or A record lookup).
- Validate the local part character set — special characters and quoted strings are not checked beyond length and the absence of spaces.
- Enforce the full label character rules from RFC 5321/5322 (e.g. digits-only labels, internationalised domain names).
- Check for disposable or role-based addresses.
- Guarantee the address belongs to a real mailbox.

For production email verification, pair this function with a DNS check or a dedicated library such as [`email-validator`](https://pypi.org/project/email-validator/).
