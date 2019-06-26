import requests
from bs4 import BeautifulSoup
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

file = 'headline_container.txt'
url = 'https://www.spiegel.de/schlagzeilen/tops/'
today = date.today()

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
headlines_spon = soup.findAll('h2', attrs = {'class':"article-title"})

contents = ''

for headline in headlines_spon:
    contents += headline.text

#Email Settings
smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "yournewsdealer@gmail.com"
password = 'kukbad-jomnU5-bugrom'
receiver_email = "jramdohr23@gmail.com"

message = MIMEMultipart("alternative")
message["Subject"] = "Schlagzeilen - " + today.strftime("%A, %d/%m/%y")
message["From"] = "Ihr Nachrichtendienst"
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = """\
    $(contents)
    """
html = """\
<html>
  <body>
    <p>Die Schlagzeilen heute:
        <span> $(contents) </span>   
    </p>
  </body>
</html>"""

text = text.replace("$(contents)", contents)
#html = html.replace("$(contents)", contents)

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
#part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
#message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
