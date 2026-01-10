import pywhatkit
import datetime

# Get current time
now = datetime.datetime.now()

# Send WhatsApp message
pywhatkit.sendwhatmsg(
    phone_no="+917799558671",   # Replace with WhatsApp number
    message="Hello! This message is sent using Python 😊",
    time_hour=now.hour,
    time_min=now.minute + 2     # Must be 1–2 minutes ahead
)

print("Message scheduled successfully!")