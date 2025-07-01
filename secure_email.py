import yagmail
import getpass
import logging
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='email_logs.log'
)

def send_email():
    try:
        print("\n=== Simple Gmail Sender ===")
        print("Note: Make sure you have your App Password ready\n")
        
        # Get email credentials
        sender_email = input("Enter your Gmail address: ")
        print("Enter your Gmail App Password (16 characters):")
        sender_password = getpass.getpass()

        # Initialize yagmail SMTP
        print("\nConnecting to Gmail...")
        yag = yagmail.SMTP(sender_email, sender_password)
        print("Connected successfully!")

        # Get email details
        print("\n--- Email Details ---")
        recipient = input("Enter recipient's email: ")
        subject = input("Enter email subject: ")
        print("Enter email message (press Enter twice when done):")
        
        # Collect message lines
        message_lines = []
        while True:
            line = input()
            if line == "":
                break
            message_lines.append(line)
        message = "\n".join(message_lines)

        # Confirm before sending
        print("\nReview your email:")
        print(f"To: {recipient}")
        print(f"Subject: {subject}")
        print(f"Message:\n{message}")
        
        confirm = input("\nSend this email? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Email cancelled.")
            return False

        # Send the email
        print("\nSending email...")
        yag.send(
            to=recipient,
            subject=subject,
            contents=message
        )

        print("✓ Email sent successfully!")
        logging.info(f"Email sent successfully to {recipient}")
        return True

    except Exception as e:
        print(f"\nError sending email: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you entered your Gmail address correctly")
        print("2. Verify that you're using the App Password, not your regular Gmail password")
        print("3. Check your internet connection")
        logging.error(f"Failed to send email: {str(e)}")
        return False

# Run the email sender
if __name__ == "__main__":
    try:
        send_email()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
    
    input("\nPress Enter to exit...") 