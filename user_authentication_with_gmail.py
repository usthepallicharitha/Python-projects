import smtplib
import random

otp = random.randint(100000, 999999)

sender_email = " charithausthepalli@gmail.com"
app_password = " nnli hhih zjmu qitx "
receiver_email = "usthepallicharithaa24@gmail.com"

message = f"Subject: OTP Verification\n\nYour OTP is {otp}"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(sender_email, app_password)
server.sendmail(sender_email, receiver_email, message)
server.quit()

print("OTP sent")

user_otp = int(input("Enter OTP: "))
if user_otp == otp:
    print("OTP verified")
else:
    print("Wrong OTP")
