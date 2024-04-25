import os
from dotenv import load_dotenv

from flask import Flask, render_template, flash, redirect, url_for, request
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


@app.route('/add_contact', methods=['POST'])
def add_contact():

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    if request.method == "POST":
        if len(request.form['name']) >= 1:

            with UseDatabase(app.config['dbconfig']) as cursor:

                query = f'''INSERT INTO {os.getenv('DATABASE')} (name, email, phone) VALUES (%s, %s, %s)'''
                cursor.execute(query, (name, email, phone))
                flash('Contact added successfully', category='success')
        else:
            flash(
                'Contact not added. Fill in the "Name" field, please!',
                category='danger',
            )

        return redirect(url_for('get_contacts'))


@app.route('/delete/<string:id_>', methods=['GET'])
def delete_contact(id_):

    with UseDatabase(app.config['dbconfig']) as cursor:

        query = f'''DELETE FROM {os.getenv('DATABASE')} WHERE id=%s'''
        cursor.execute(query, (id_,))
        flash('Contact has been deleted successfully', category='success')

    return redirect(url_for('get_contacts'))


@app.route('/update_contact', methods=['POST', 'GET'])
def update_contact():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        with UseDatabase(app.config['dbconfig']) as cursor:

            query = f'''
        UPDATE {os.getenv('DATABASE')} SET name=%s, email=%s, phone=%s
        WHERE id=%s
        '''
            cursor.execute(
                query,
                (
                    name,
                    email,
                    phone,
                    id,
                ),
            )
        flash('Contact updated successfully', category='success')

        return redirect(url_for('get_contacts'))


if __name__ == '__main__':
    app.run(debug=True)
