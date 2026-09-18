import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

def send_email(report_content):
    # 1. Force reload the .env file to ensure the latest credentials are used
    load_dotenv() 
    
    sender_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASS") 
    receiver_email = "stevenmarcos10@yahoo.com"

    # 2. DEBUG CHECK: Immediate feedback if the .env isn't loading correctly
    if not sender_email or not app_password:
        print("   ⚠️ ERROR: .env file missing or EMAIL_USER/PASS not found!")
        return

    # 3. Setup the Email Message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "💰 Price Tracker Update"
    msg.attach(MIMEText(report_content, 'plain'))

    # 4. Attempt to connect and send
    try:
        # Use port 587 for TLS (standard for Gmail)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        
        # DEBUG LEVEL: Prints the conversation between your computer and Gmail
        # Helpful for identifying if Google is blocking your IP or Password
        server.set_debuglevel(1) 
        
        server.starttls() # Secure the connection
        
        # Log in and send
        server.login(sender_email, app_password)
        server.send_message(msg)
        
        server.quit() # Cleanly close the connection
        print("   📧 Email report sent successfully!")
        
    except Exception as e:
        # Prints the specific error (e.g., Auth failure, Connection timeout)
        print(f"   ⚠️ Failed to send email: {e}")