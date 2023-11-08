#by jiakai
import pyotp
import qrcode

# Generate a secret key for Time-based One-Time Password (TOTP)
totp = pyotp.TOTP(pyotp.random_base32())
secret = totp.secret
print(f"Your secret key is: {secret}")
# Generate the current TOTP code
current_totp = totp.now()
print(f"Your current TOTP is: {current_totp}")
# This is the QR code that you can provide to the user.
qr_code_url = totp.provisioning_uri(name='AaronJiakai', issuer_name='testService')
print(f"Scan this QR Code in your TOTP client: {qr_code_url}")
# Generate and save the QR code image
qrcode.make(qr_code_url).save("totp.png")


# Simulate user input testing
user_input_totp = input("Enter the TOTP from your app: ")
# Verify if the user input TOTP is correct
if totp.verify(user_input_totp):
    print("The TOTP is correct.")
else:
    print("The TOTP is incorrect.")
