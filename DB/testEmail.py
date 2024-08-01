import smtplib
from email.mime.text import MIMEText


def verify_email(email, smtp_server='smtp.gmail.com', smtp_port=587):
    try:
        # Create an SMTP connection
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            # Start the TLS connection
            smtp.starttls()

            # Send the "VRFY" command to verify the email address
            smtp.ehlo()
            code, message = smtp.verify(email)

            # Check the response code
            if code == 250:
                return True, message
            else:
                return False, message
    except Exception as e:
        return False, str(e)


email_to_verify = "abebe@gmail.com"
is_valid, message = verify_email(email_to_verify)

if is_valid:
    print(f"Email '{email_to_verify}' is valid: {message}")
else:
    print(f"Email '{email_to_verify}' is invalid: {message}")
