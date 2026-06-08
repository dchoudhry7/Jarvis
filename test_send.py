from tools.email_tools import send_email

print(
    send_email.invoke(
        {
            "recipient": "YOUR_OTHER_EMAIL@gmail.com",
            "subject": "Jarvis Test",
            "body": "Testing Gmail API"
        }
    )
)