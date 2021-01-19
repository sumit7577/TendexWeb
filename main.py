from flask import Flask,render_template,request,url_for,redirect,flash
from flask_sqlalchemy import  SQLAlchemy
import stripe
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired,Length,ValidationError
from flask_mail import Mail
from flask_login import LoginManager,login_user,current_user,logout_user,UserMixin

app = Flask(__name__)
db = SQLAlchemy(app)
app.secret_key = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51HpQavLo9p3SVh7eOClO69TFk12K8XQAoDWwjoww6tPw8hsSJommJMfe2hMxtQef9DRArVwu1wrdeWTcXNtyjkOE00n0IgeqT4'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51HpQavLo9p3SVh7eqAAvUYsQbi8F46rk9Qk55osFFjDZqhZL5KQSz42rHMibylbAiSTiUM0pQ9PwRIGhesXfhJns00RPqL0xSA'
app.config["SQLALCHEMY_DATABASE_URI"]= "mysql://sumitkumar:idontknow@1@sumitkumar.mysql.pythonanywhere-services.com/sumitkumar$tendex"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
app.config.update(MAIL_SERVER="smtp.gmail.com",
MAIL_PORT="465",
MAIL_USE_SSL="True",
MAIL_USERNAME="ultroncustomercare@gmail.com",
MAIL_PASSWORD="jaykambli4465")
mail = Mail(app)
stripe.api_key = app.config["STRIPE_SECRET_KEY"]
#initalize login manager
login = LoginManager(app)
login.init_app(app)


class Registration(FlaskForm):
	username = StringField('username', validators=[InputRequired(message="Username required"), Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
	email = EmailField("email", validators=[InputRequired("Please Enter valid email address")])
	
class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(12), unique=True, nullable=False)
	email = db.Column(db.String(), nullable=False, unique = False)

class Key(db.Model):
	__tablename__ = "sumitwa"
	id = db.Column(db.Integer, primary_key=True)
	key7 = db.Column(db.String(20), unique=True, nullable=False)
	key15 = db.Column(db.String(20), nullable=False, unique = True)
	key30 = db.Column(db.String(20), unique=True, nullable=False)
	key60 = db.Column(db.String(20), nullable=False, unique = True)

class Login(db.Model,UserMixin):
	__tablename__ = "Admin"
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.String(12), unique=True, nullable=False)
	password = db.Column(db.String(), nullable=False, unique = True)
	key7amount = db.Column(db.Integer,nullable=True,unique=False)
	key15amount = db.Column(db.Integer,nullable=True,unique=False)
	key30amount=db.Column(db.Integer,nullable=True,unique=False)
	key60amount=db.Column(db.Integer,nullable=True,unique=False)


@app.route("/")
def home():
	return render_template("index.html")

@app.route("/pay", methods = ["GET", "POST"])
def pay():
	reg_form = Registration()
	if reg_form.validate_on_submit():
		username = reg_form.username.data
		email = reg_form.email.data
		user = User(username = username, email= email)
		db.session.add(user)
		db.session.commit()
		mail.send_message("New 7 Day Key Order From "+ username, sender= email, recipients=["ultroncustomercare@gmail.com"],body = "7 Day order key placed from "+ username + "\n" + "sender: " + email + "+\n" + "Please Check Your Stripe account for successed payments")
	return render_template("register.html", reg_form = reg_form)
	
@app.route("/pay1", methods = ["GET", "POST"])
def pay1():
	reg_form = Registration()
	if reg_form.validate_on_submit():
		username = reg_form.username.data
		email1 = reg_form.email.data
		user = User(username = username, email= email1)
		db.session.add(user)
		db.session.commit()
		mail.send_message("New 15 Day Key Order From "+ username, sender= email1, recipients=["ultroncustomercare@gmail.com"],body = "15 Day order key placed from"+ username + "\n" + "sender: " + email1 + "+\n" + "Please Check Your Stripe account for successed payments")
	return render_template("register2.html", reg_form = reg_form)
	
@app.route("/pay2", methods = ["GET", "POST"])
def pay2():
	reg_form = Registration()
	if reg_form.validate_on_submit():
		username = reg_form.username.data
		email2 = reg_form.email.data
		user = User(username = username, email= email2)
		db.session.add(user)
		db.session.commit()
		mail.send_message("New 30 Day Key Order From "+ username, sender= email2, recipients=["ultroncustomercare@gmail.com"],body = "30 Day order key placed from"+ username + "\n" + "sender: " + email2 + "+\n" + "Please Check Your Stripe account for successed payments")
	return render_template("register3.html", reg_form = reg_form)
	
@app.route("/pay3", methods = ["GET", "POST"])
def pay3():
	reg_form = Registration()
	if reg_form.validate_on_submit():
		username = reg_form.username.data
		email3 = reg_form.email.data
		user = User(username = username, email= email3)
		db.session.add(user)
		db.session.commit()
		mail.send_message("New 60 Day Key Order From "+ username, sender= email3, recipients=["ultroncustomercare@gmail.com"],body = "60 Day order key placed from"+ username + "\n" + "sender: " + email3 + "+\n" + "Please Check Your Stripe account for successed payments")
	return render_template("register4.html", reg_form = reg_form)

@app.route('/stripe_pay')
def stripe_pay():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1HwgOMLo9p3SVh7eKHPyKzRj',
            'quantity': 1,
        }
        ],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('home', _external=True),
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }
 
@app.route('/stripe_pay1')
def stripe_pay1():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
        {"price":
        "price_1HwgN9Lo9p3SVh7e5U4m1NHf",
        "quantity":1},
        ],
        mode='payment',
        success_url=url_for('thanks1', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('home', _external=True),
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }

@app.route('/stripe_pay2')
def stripe_pay2():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
        {"price":
        "price_1HwgPbLo9p3SVh7egrNMJVpj",
        "quantity":1}
        ],
        mode='payment',
        success_url=url_for('thanks2', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('home', _external=True),
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }
 
@app.route('/stripe_pay3')
def stripe_pay3():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
        {"price":
        "price_1HwgQDLo9p3SVh7e9SbXXwQS",
        "quantity":1}
        ],
        mode='payment',
        success_url=url_for('thanks3', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('home', _external=True),
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }

@app.route("/thanks")
def thanks():
    	if(stripe_pay == True):
    		post = Key.query.limit(1).all()
    		return render_template("thanks.html",post=post)
    	else:
    	   return redirect(url_for("home"))
    	   
@app.route("/thanks1")
def thanks1():
    	if(stripe_pay1 == True):
    		post = Key.query.limit(1).all()
    		return render_template("thanks1.html",post=post)
    	else:
    	   return redirect(url_for("home"))
    	   
@app.route("/thanks2")
def thanks2():
    	if(stripe_pay2 == True):
    		post = Key.query.limit(1).all()
    		return render_template("thanks2.html",post=post)
    	else:
    	   return redirect(url_for("home"))
    	   
@app.route("/thanks3")
def thanks3():
    	if(stripe_pay3 == True):
    		post = Key.query.limit(1).all()
    		return render_template("thanks3.html",post=post)
    	else:
    	   return redirect(url_for("home"))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@login.user_loader
def load_user(id):
	return Login.query.filter_by(id=id).first()
	

#validate username
def validate_username(form,field):
	password = field.data
	username = form.username.data
	user_data = Login.query.filter_by(user=username).first()
	if user_data is None:
		raise ValidationError("Username or password incorrect")
	elif(password != user_data.password):
		raise ValidationError("Username or password incorrect")
		
class Admins(FlaskForm):
	username = StringField('name', validators=[InputRequired(message="Username required"), Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
	password = PasswordField("password", validators=[InputRequired("password required"),validate_username])

class reseller(FlaskForm):
	username = StringField('name', validators=[InputRequired(message="Username required"), Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
	password = PasswordField("password", validators=[InputRequired("password required")])

	
@app.route("/login",methods=["GET","POST"])
def loginadmin():
	login_form = Admins()
	if login_form.validate_on_submit():
		user_object = Login.query.filter_by(user =login_form.username.data).first()
		login_user(user_object)
		if current_user.user == "admin":
			return redirect(url_for("dashboard"))
		return  redirect(url_for("dashboard2"))
				
	return render_template("login.html", form = login_form)

@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
	reg_form = reseller()
	if not current_user.is_authenticated:
		return redirect(url_for("home"))
	users = Login.query.filter_by().all()
	if reg_form.validate_on_submit():
		reselluser = reg_form.username.data
		resellpass = reg_form.password.data
		resell = Login(user=reselluser,password=resellpass)
		db.session.add(resell)
		db.session.commit()
		flash("User Added successfully","success")
	return render_template("resell.html",user=current_user.user,users=users,reg_form=reg_form)
	
@app.route("/dashboard2")
def dashboard2():
	if current_user.is_authenticated:	
		data = Login.query.filter_by(id=current_user.id).first()
		keys = Key.query.limit(data.key7amount).all()
		keys2 = Key.query.limit(data.key15amount).all()
		keys3 = Key.query.limit(data.key30amount).all()
		keys4 = Key.query.limit(data.key60amount).all()
		return render_template("dashboard2.html",user=current_user.user,data=data,keys=keys,keys2=keys2,keys3=keys3,keys4=keys4)
	return redirect(url_for("home"))


@app.route("/delete/<string:id>",methods=["GET","POST"])
def delete(id):
	if current_user.is_authenticated and current_user.user == "admin":
		admins = Login.query.filter_by(id=id).first()
		db.session.delete(admins)
		db.session.commit()
		flash("User deleted successfully","success")
	return redirect(url_for("dashboard"))


@app.route("/add/<string:id>",methods=["GET","POST"])
def add(id):
	if not current_user.is_authenticated and current_user.user != "tendex":
		return redirect(url_for("home"))
	posts = Login.query.filter_by(id=id).first()
	if(request.method=="POST"):
		key7amoun = request.form.get("key7uname")
		key15amoun = request.form.get("key15uname")
		key30amoun = request.form.get("key30uname")
		key60amoun = request.form.get("key60uname")
		posts.key7amount = key7amoun
		posts.key15amount = key15amoun
		posts.key30amount = key30amoun
		posts.key60amount = key60amoun
		db.session.commit()
		flash("Key Succesfully Added and updated","success")
		return render_template("edit.html",posts=posts)
				

@app.route("/logout")
def logout():
	logout_user()
	flash("You have been logged out successfully","sucess")
	return redirect(url_for("loginadmin"))
	
if __name__=="__main__":
	app.run()

