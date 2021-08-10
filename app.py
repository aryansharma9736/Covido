import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = '1'
#######################################################################
#######################################################################
from form import  AddForm , DelForm
from flask import Flask, redirect, url_for, render_template,request, session
from flask_dance.contrib.google import make_google_blueprint, google
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import stripe;
import requests
from pygame import mixer 
from datetime import datetime, timedelta
import time


app = Flask(__name__)

public_key = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'
stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)






blueprint = make_google_blueprint(
    client_id="674058017740-c7rgfosf7nmr746m6q9p7he7e9bphpl9.apps.googleusercontent.com",
    client_secret="vKFrPFwI8KRH2PGCwauel2z1",
    # reprompt_consent=True,
    offline=True,
    scope=["profile", "email"]
)
app.register_blueprint(blueprint, url_prefix="/login")

class Info(db.Model):

    __tablename__ = 'info'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.Text)
    beds = db.Column(db.Integer)
    cylinder = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    source_name = db.Column(db.Text)
    numbers = db.Column(db.Integer)

    def __init__(self,id,name,beds,cylinder,phone,source_name,numbers):
        self.id = id
        self.name = name
        self.beds = beds
        self.cylinder = cylinder
        self.phone = phone
        self.source_name = source_name
        self.numbers = numbers

    def __repr__(self):
        return f" ID of the record : {self.id},\n Name of the hospital : {self.name},\n No. beds available :{self.beds},\n No. of cylinders : {self.cylinder},\n Contact number of hospital : {self.phone},\n Name of the source : {self.source_name},\n Contact of the source : {self.numbers}"
       

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/action')
def action():

    info = Info.query.all()
    return render_template('action.html', info=info)

@app.route('/add_hospital', methods=['GET', 'POST'])
def add_hospital():
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email=resp.json()["email"]
    form = AddForm()

    if form.validate_on_submit():
        


        # Add new Hospital to database
        new_hospital = Info(id  = form.id.data,name = form.name.data,beds = form.beds.data,cylinder = form.cylinder.data,
                                  phone = form.phone.data,
                                  source_name = form.source_name.data,numbers = form.numbers.data)
        db.session.add(new_hospital)
        db.session.commit()

        return redirect(url_for('action'))

    return render_template('add_hospital.html',form=form)


@app.route('/del_hospital', methods=['GET', 'POST'])
def del_hospital():

    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        hospital = Info.query.get(id)
        db.session.delete(hospital)
        db.session.commit()

        return redirect(url_for('action'))
    return render_template('del_hospital.html',form=form)



    
@app.route('/doctors')
def doctors():
    return render_template('doctors.html')

@app.route('/news')
def news():
    return render_template('news.html',public_key=public_key)


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/payment', methods=['POST'])
def payment():

    # CUSTOMER INFORMATION
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    # CHARGE/PAYMENT INFORMATION
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=2000,
        currency='usd',
        description='Donation'
    )

    return redirect(url_for('thankyou'))
@app.route('/form')
def form():
    

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email=resp.json()["email"]

    return render_template("form.html",email=email)


@app.route("/login/google")
def login():
    if not google.authorized:
        return render_template(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email=resp.json()["email"]

    return render_template("action.html",email=email)

if __name__ ==  '__main__':
    app.run(debug=True) 