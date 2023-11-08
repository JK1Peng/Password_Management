#by jiakai
import re

def validate_password_strength(password):

    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None  # At least one digit
    uppercase_error = re.search(r"[A-Z]", password) is None  # At least one uppercase letter
    lowercase_error = re.search(r"[a-z]", password) is None  # At least one lowercase letter
    symbol_error = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is None  # At least one special character
    space_error = re.search(r"\s", password) is not None  # No whitespace allowed
    complexity_error = re.fullmatch(r"(.)\1*", password) is not None  # Checks if the password is not all the same character

    common_passwords = ["password", "123456", "12345678","qwerty"] # can add latert
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

# test
# password_test = validate_password_strength("AaronJiakai123!")
# print("good password??", password_test["password_ok"])
# print("Errors:", password_test["errors"])
