from flask import Flask, render_template, request
from sqlalchemy import create_engine
from werkzeug.serving import WSGIRequestHandler
import pandas as pd

app = Flask(__name__)

# Helper Functions
def engine_generator(source):
    # Database connection info. Note that this is not a secure connection.
    username = 'root'
    password = 'Faq76628'
    host = '127.0.0.1'
    port = '3306'
    db_name = source

    # CONNECTOR TO DB
    connecor_url = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(username, password, host, port, db_name)
    engine = create_engine(connecor_url)
    return engine

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":

        contact_name = request.form['name']
        contact_email = request.form['email']
        contact_subject = request.form['subject']
        contact_message = request.form['message']

        contact = {
            'Name': [contact_name],
            'Email': [contact_email],
            'Subject': [contact_subject],
            'Message': [contact_message]
        }

        df = pd.DataFrame.from_dict(contact)
        df.columns = ['Name', 'Email', 'Subject', 'Message']

        df.to_sql('MESSAGES', con=engine_generator('flask_test'), if_exists='append', index=False)
    return render_template('index.html')



if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True)