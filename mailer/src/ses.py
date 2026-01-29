import os
from typing import Dict

import boto3


def send_email(to_email: str, subject: str, html: str, text: str) -> Dict[str, str]:
    client = boto3.client("ses", region_name=os.environ.get("SES_REGION", "us-east-1"))
    response = client.send_email(
        Source=os.environ.get("MAILER_FROM", "signals@example.com"),
        Destination={"ToAddresses": [to_email]},
        Message={
            "Subject": {"Data": subject},
            "Body": {
                "Html": {"Data": html},
                "Text": {"Data": text},
            },
        },
    )
    return {"message_id": response.get("MessageId", "")}
