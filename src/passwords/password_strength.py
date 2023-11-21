from zxcvbn import zxcvbn
import re


def password_check(password, domain="", username=""):
    strength = measure_password_strength(password, domain, username)
    valid = validate_password_characteristics(password)
    if not valid["password_ok"]:
        errors = valid["errors"]
        for key in errors.keys():
            print(key, errors[key])
            if errors[key]:
                return key
    else:
        if strength < 3:
            return "too common, or simple"
    return True


def measure_password_strength(password, domain="", username=""):
    results = zxcvbn(password, user_inputs=[domain, username])
    return results["score"]
    # results["crack_times_seconds"]["offline_fast_hashing_1e10_per_second"]


def validate_password_characteristics(password):

    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None  # At least one digit
    uppercase_error = re.search(r"[A-Z]", password) is None  # At least one uppercase letter
    lowercase_error = re.search(r"[a-z]", password) is None  # At least one lowercase letter
    symbol_error = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is None  # At least one special character
    space_error = re.search(r"\s", password) is not None  # No whitespace allowed
    complexity_error = re.fullmatch(r"(.)\1*",
                                    password) is not None  # Checks if the password is not all the same character

    common_passwords = ["password", "123456", "12345678", "qwerty"]  # can add later
    common_password_error = password in common_passwords

    good_password = not (length_error or digit_error or uppercase_error or
                         lowercase_error or symbol_error or space_error or
                         common_password_error or complexity_error)

    # Return the result
    return {
        "password_ok": good_password,
        "errors": {
            "length_error": length_error,
            "digit_error": digit_error,
            "uppercase_error": uppercase_error,
            "lowercase_error": lowercase_error,
            "symbol_error": symbol_error,
            "space_error": space_error,
            "common_password_error": common_password_error,
            "complexity_error": complexity_error,
        }
    }
