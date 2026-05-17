#!/usr/bin/env python3

import json
import re
import sys

_EMAIL_PATTERN = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")


def validate_email(email: str) -> tuple[bool, str]:
    normalized_email = email.strip()
    if not normalized_email:
        return False, "Email cannot be empty."

    if _EMAIL_PATTERN.match(normalized_email):
        return True, "Valid email format."

    return False, f"'{normalized_email}' is not a valid email format. A valid domain is required."


def _result_payload(*, email: str, is_valid: bool, message: str) -> dict[str, object]:
    return {
        "type": "email",
        "email": email,
        "is_valid": is_valid,
        "message": message,
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(
            json.dumps(
                {
                    "type": "email",
                    "email": "",
                    "is_valid": False,
                    "message": "Usage: python validate_email.py <email>",
                }
            )
        )
        return 1

    email = argv[1]
    is_valid, message = validate_email(email)

    print(
        json.dumps(
            _result_payload(
                email=email,
                is_valid=is_valid,
                message=message,
            )
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
