from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, redirect, request
from datetime import datetime
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Bootstrap(app)
scheduler = BackgroundScheduler()


class Contact(db.Model):
    id = db.Column('Contact_id', db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(80), unique=False, nullable=True)
    surname = db.Column(db.String(80), unique=False, nullable=True)
    emails = db.relationship('NewEmail', backref='contact', lazy=True, cascade="all,delete")
    created_at = db.Column(
        db.DateTime, unique=False, nullable=False, default=datetime.utcnow,
    )

    def __init__(self, username, email, first_name, surname):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.surname = surname


class NewEmail(db.Model):
    id = db.Column('Email_id', db.Integer, primary_key=True)
    new_email = db.Column(db.String(120), unique=True, nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.Contact_id'), nullable=False)

    def __init__(self, new_email, contact_id):
        self.new_email = new_email
        self.contact_id = contact_id


db.create_all()
db.session.commit()


@app.route('/')
def home():
    return render_template(
        'home.html', contacts=Contact.query.all(),
        scheduler_status=scheduler.state,
    )


@app.route('/start-scheduler')
def start_scheduler():
    if not scheduler.state:
        scheduler.add_job(create_a_contact, 'interval', seconds=5)
        scheduler.add_job(delete_a_contact, 'interval', minutes=1)
        scheduler.start()
    else:
        scheduler.shutdown()

    return redirect("/")


@app.route('/create')
def create_contact():
    return render_template('contact.html')


@app.route('/update/<int:contact_id>', methods=['GET'])
def update_contact(contact_id):
    contact = Contact.query.get(contact_id)
    return render_template('update.html', contact=contact)


@app.route('/delete/<int:contact_id>')
def delete(contact_id):
    contact = Contact.query.get(contact_id)
    db.session.delete(contact)
    db.session.commit()

    return redirect("/")


@app.route('/save', methods=['POST'])
def save_contact(contact_id=None):
    try:
        if contact_id:
            contact = Contact.query.get(contact_id)
            contact.username = request.form['name']
            contact.email = request.form['email']
            contact.first_name = request.form['first']
            contact.surname = request.form['surname']

        else:
            username = request.form['username']
            email = request.form['email']
            first = request.form['first']
            surname = request.form['surname']

            contact = Contact(username, email, first, surname)
            db.session.add(contact)

        db.session.commit()
        msg = "Successfully created"

    except Exception:
        msg = "Error"

    return render_template("result.html", data=[msg])


@app.route('/get-email', methods=['GET'])
def get_email():
    return render_template('new_email.html')


@app.route('/add-new-email/<int:contact_id>')
@app.route('/add-new-email', methods=['POST'])
def add_email(contact_id=None):
    if request.method == 'POST':
        contact_id = Contact.query.filter_by(email=request.form['email']).first().id
    data = {
        'create': True,
        'contact_id': contact_id,
    }
    return render_template('new_email.html', data=data)


@app.route('/add-new-email/<int:contact_id>', methods=['POST'])
def save_new_email(contact_id):
    email = request.form['email']
    new_email = NewEmail(email, contact_id)
    db.session.add(new_email)
    db.session.commit()
    msg = "Successfully created"

    return render_template("result.html", data=[msg])


@app.route('/selected-email/<int:email_id>', methods=['GET'])
def select_email(email_id):
    return render_template('new_email.html', email=NewEmail.query.get(email_id))


@app.route('/update-email/<int:email_id>', methods=['POST'])
def update_email(email_id):
    email = NewEmail.query.get(email_id)
    email.new_email = request.form['email']
    db.session.commit()
    return redirect("/")


def create_a_contact():
    username = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
    email = ''.join(random.choice(string.ascii_lowercase) for x in range(10)) + '@gmail.com'
    contact = Contact(username, email, first_name=None, surname=None)
    db.session.add(contact)
    db.session.commit()

    new_email = ''.join(random.choice(string.ascii_lowercase) for x in range(10)) + '@abv.com'
    db.session.add(NewEmail(new_email, contact.id))
    db.session.commit()


def delete_a_contact():
    db.session.delete(Contact.query.first())
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
