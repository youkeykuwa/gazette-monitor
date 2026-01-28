import requests
from bs4 import BeautifulSoup
import os

# URL to monitor
URL = "https://www.city.fuchu.tokyo.jp/gyosei/johokokai/koho/kohoshi/koho/reiwa8nenhakkou/index.html"

# file that stores the prior content
LAST_FILE = "last_snapshot.txt"

# fetch page
resp = requests.get(URL)
content = resp.text

# compare with previous
if os.path.exists(LAST_FILE):
    with open(LAST_FILE, "r", encoding="utf-8") as f:
        previous = f.read()
else:
    previous = ""

# if changed, send email
if content != previous:
    import smtplib
    from email.mime.text import MIMEText

    SMTP_SERVER = os.environ["SMTP_SERVER"]
    SMTP_PORT   = int(os.environ["SMTP_PORT"])
    EMAIL_USER  = os.environ["EMAIL_USER"]
    EMAIL_PASS  = os.environ["EMAIL_PASS"]
    TO_EMAIL    = os.environ["TO_EMAIL"]

    msg = MIMEText(f"Fuchu Gazette page changed! URL:\n{URL}")
    msg["Subject"] = "📢 Fuchu Gazette Update"
    msg["From"] = EMAIL_USER
    msg["To"] = TO_EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

    # update snapshot
    with open(LAST_FILE, "w", encoding="utf-8") as f:
        f.write(content)
