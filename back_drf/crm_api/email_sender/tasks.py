import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time
from celery import shared_task
from .config import *


@shared_task
def send_emails(emails_list, title, msg, file_path):
    time.sleep(1)

    # Connect with the server
    print("Connecting to server...")
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls()
    TIE_server.login(email_from, pswd)
    print("Successfully connected to server")
    print()

    emails_list = emails_list.split(',')
    for person in emails_list:
        body = msg

        # Make a MIME object to define parts of the email
        email_msg = MIMEMultipart()
        email_msg['From'] = email_from
        email_msg['To'] = person
        email_msg['Subject'] = title

        # Attach the body of the message
        email_msg.attach(MIMEText(body, 'plain'))

        if file_path is not None:
            # Open the file in python as a binary
            with open(file_path, 'rb') as attachment:
                attachment_package = MIMEBase('application', 'octet-stream')
                attachment_package.set_payload(attachment.read())
                encoders.encode_base64(attachment_package)
                attachment_package.add_header('Content-Disposition',
                                              f'attachment; filename="{os.path.basename(file_path)}"')
                email_msg.attach(attachment_package)

        # Cast as string
        text = email_msg.as_string()

        # Send email
        print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, person, text)
        print(f"Email sent to: {person}")
        print()

    # Close the server connection
    TIE_server.quit()
    print(file_path)

    # Remove the temporary file
    if file_path is not None:
        os.remove(file_path)
