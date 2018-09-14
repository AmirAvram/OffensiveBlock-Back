from flask import Flask, request
from flask import Response
from FBClassifier import predict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
import json

app = Flask(__name__)
MAX_WANTED_TUPLE_VALUE = 0.7
ADMIN_EMAIL = 'marzuckerberg@fb.com'
RECIVER_EMAIL = 'etkeren@gmail.com'
SMTP_SERVER = 'mxout.tau.ac.il'
SMTP_SERVER_NAME = "smtp.gmail.com"
SMTP_SERVER_PORT = 465


@app.route('/', methods=['GET', 'OPTIONS'])
def hello():
    results = predict(request.args.get('text'))
    if max_tuple_larger_then_wanted(get_max_tuple(results)):
        resp = Response(json.dumps({
            "bad_content": str(request.args.get('text')),
            "bad_words": ['bad']
        }))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = '*'
        send_email(msg=create_mail_msg(request.args.get('text')))
        return resp
    resp = Response(json.dumps({
    }))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp


def create_mail_msg(content):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Alert! Bad Language on FBHackathonMessenger"
    msg['From'] = ADMIN_EMAIL
    msg['To'] = RECIVER_EMAIL
    html = """\
    <html>
      <head></head>
      <body>
           <center>
            The user Message:
            {}
           </center>
           Some options to consider:
           <ul>
            <li>
                Send the user a message <a href="https://arcane-crag-36061.herokuapp.com/">Click Here</a>.
            </li>
            <li>
                Block the user from the group <a href="https://arcane-crag-36061.herokuapp.com/b">Click Here</a>.
            </li> 
            <li>
                Report the user to and Facebook administrator <a href="https://arcane-crag-36061.herokuapp.com/">Click Here</a>.
            </li>
           </ul> 
      </body>
    </html>
    """.format(content)
    part = MIMEText(html, 'html')
    msg.attach(part)
    return msg


def max_tuple_larger_then_wanted(tup):
    if tup[1] > MAX_WANTED_TUPLE_VALUE:
        return True
    return False


def get_max_tuple(tuples):
    max_tuple = None
    for tup in tuples:
        if max_tuple is not None and tup[1] > max_tuple[1]:
            max_tuple = tup
        elif max_tuple is None:
            max_tuple = tup
    return max_tuple


def send_email(msg):
    s = SMTP_SSL(SMTP_SERVER_NAME, SMTP_SERVER_PORT)
    s.login('FBTelHack2018@gmail.com', '25^okmuZ@b%MswZ^la3uu#$6')
    s.sendmail(ADMIN_EMAIL, RECIVER_EMAIL, msg.as_string())
    s.quit()


if __name__ == '__main__':
    app.run()

# def run(var, var2):
#     print(str(var) + " what " + str(var2))
#     app.run(host="0.0.0.0", port=5000)
