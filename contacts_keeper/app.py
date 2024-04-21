import os
from dotenv import load_dotenv

from flask import Flask, render_template
from dbcm import UseDatabase

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

app.config['dbconfig'] = {
    'host': os.getenv('HOST'),
    'user': os.getenv('USERNAME'),
    'password': os.getenv('PASSWORD'),
    'database': os.getenv('DATABASE'),
}


@app.route('/')
def get_contacts():
    with UseDatabase(app.config['dbconfig']) as cursor:

        query = f'''SELECT * FROM {os.getenv('DATABASE')}'''
        cursor.execute(query)

        title = 'Contacts keeper'
        contacts = cursor.fetchall()

        return render_template('entry.html', the_title=title, the_contacts=contacts)


if __name__ == '__main__':
    app.run(debug=True)
