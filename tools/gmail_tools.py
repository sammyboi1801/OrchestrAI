from langchain_core.tools import tool
from dotenv import load_dotenv
import yagmail
import os
from imap_tools import MailBox
import json

load_dotenv()


@tool
def SEND_GMAIL(recipients: list[str] , subject: str, message: str) -> str:
    """
    This tool can be used to send mail to any email ID
    :param recipients: list of email ID for sending email
    :param subject: Subject of the mail
    :param message: Body of the mail
    :return: Error or sent status
    """

    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PASS = os.getenv('EMAIL_PASS')

    msg = message + "\n\n ---Message automated by KAI :)"

    yag = yagmail.SMTP(EMAIL_HOST, EMAIL_PASS)

    try:
        yag.send(
            to = recipients,
            subject = subject,
            contents = msg
        )
        status_msg = "Email sent successfully"
    except Exception as e:
        status_msg = f"An error occured: {e}"

    return status_msg


@tool
def READ_GMAIL(fetch_limit: int) -> dict:
    """
    This tool can be used to read mails that the user has received.
    :param fetch_limit: No. of recent emails to fetch
    """

    mails = {}

    try:
        with MailBox("imap.gmail.com").login(username=os.getenv("EMAIL_HOST"), password=os.getenv("EMAIL_PASS"),
                                             initial_folder="Inbox") as mb:
            count = 0
            for msg in mb.fetch(limit=fetch_limit, reverse=True, mark_seen=False):
                mail = {
                    "Date": str(msg.date),
                    "From": msg.from_,
                    "Subject": msg.subject,
                    "Content": msg.text,
                    "Flag": msg.flags
                }
                mails[count] = mail
                count += 1
    except Exception as e:
        mails = {"Error": e}

    with open('result.json', 'w') as fp:
        json.dump(mails, fp)

    return mails if mails != {} else "No mails!"