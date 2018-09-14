from flask import Flask, request
from flask import Response
from FBClassifier import predict
import json

app = Flask(__name__)
MAX_WANTED_TUPLE_VALUE = 0.7
ADMIN_EMAIL = 'marzuckerberg@fb.com'
SMTP_SERVER = 'mxout.tau.ac.il'
SMTP_SERVER_NAME = "smtp.gmail.com"
SMTP_SERVER_PORT = 587


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
        send_email(smtp_server=SMTP_SERVER, sender=ADMIN_EMAIL,
                   receiver='amiravrm@gmail.com', subject='Hi...',
                   content='who did you call mother fucker?!')
        return resp
    resp = Response(json.dumps({
    }))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp


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


def send_email(smtp_server, sender, receiver, subject='', content=''):
    from email.mime.text import MIMEText
    from smtplib import SMTP
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    s = SMTP()
    s.connect(SMTP_SERVER_NAME, SMTP_SERVER_PORT)
    s.starttls()
    s.send_message(msg)
    s.quit()


if __name__ == '__main__':
    # app.run()
    pass


send_email(smtp_server=SMTP_SERVER, sender=ADMIN_EMAIL,
           receiver='amiravrm@gmail.com', subject='Hi...',
           content='who did you call mother fucker?!')


def run(var, var2):
    print(str(var) + " what " + str(var2))
    app.run(host="0.0.0.0", port=5000)
