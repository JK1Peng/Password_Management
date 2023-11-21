"""
File: src/passwords/password_strength.py

Author: Aaron Kersten, Jiakai Peng

Description: Checks the strength of a password based on specific criteria,
             and using zxcvbn.
"""

from zxcvbn import zxcvbn
import re


"""
@param: password: password to check
@param: domain: associated domain
@param: username: associated username
@return: True for valid password, or
         message to describe why it was marked invalid
         
Uses both measures of strength measure--criteria and zxcvbn to verify that
the password is strong.
"""
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


"""
@param: password: password to check
@param: domain: associated domain
@param: username: associated username
@return: strength score in range [0, 5)

Measures password strength using zxcvbn.
"""
def measure_password_strength(password, domain="", username=""):
    try:
        results = zxcvbn(password, user_inputs=[domain, username])
        return results["score"]
    except Exception as e:
        return 0


"""
@param: password: password to check
@return: True for valid password, or
         message to describe why it was marked invalid
         
Checks password against a set of criteria.
"""
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
