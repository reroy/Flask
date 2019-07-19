from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Contact.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


class Contact(db.Model):
    id = db.Column('Contact_id', db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)

    def __init__(self, username, email, first_name, surname):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.surname = surname

    def __repr__(self):
        return '<User %r>' % self.username


db.create_all()
db.session.commit()


@app.route('/')
def home():
    return render_template('home.html', contacts=Contact.query.all())


@app.route('/enternew')
def new_contact():
    return render_template('contact.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            first = request.form['first']
            surname = request.form['surname']

            contact = Contact(name, email, first, surname)
            db.session.add(contact)
            db.session.commit()
            msg = "Successfully created"

        except:
            msg = "Error"

        return render_template("result.html", msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
