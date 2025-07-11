import pandas as pd
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load Excel
df = pd.read_excel('emails.xlsx')  # Replace with your file name
df = df.dropna(subset=['From Email', 'To Email'])

# Track current logged-in from email
current_from_email = None
server = None

# Function to convert email to env variable key format
def email_to_env_key(email):
    return email.lower().replace('@', '_').replace('.', '_')

# Email content
subject = 'Automated Mail'
body = '''Hi,

This is a test email sent via Python SMTP script.

Regards,
Your Team
'''

for index, row in df.iterrows():
    from_email = row['From Email']
    to_email = row['To Email']

    if from_email != current_from_email:
        # Close previous server if open
        if server:
            server.quit()

        # Get password from .env using transformed key
        env_key = f"EMAIL_PASSWORD_{email_to_env_key(from_email)}"
        password = os.getenv(env_key)

        if not password:
            print(f"Password not found for {from_email} in .env file!")
            continue

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, password)
            print(f"Logged in with {from_email}")
            current_from_email = from_email
        except Exception as e:
            print(f"Failed to login with {from_email}: {e}")
            continue

    # Compose and send email
    msg = EmailMessage()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        server.send_message(msg)
        print(f"Email sent from {from_email} to {to_email}")
    except Exception as e:
        print(f"Failed to send email from {from_email} to {to_email}: {e}")

# Close server at end
if server:
    server.quit()
