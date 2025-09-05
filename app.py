import flask
from flask import Flask, jsonify, request, redirect, url_for, flash
from flask import render_template
from forms import ContactUsForum, VehicleForm, LoginForm
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models import User, Vehicle, admin_user

app = Flask(__name__)

# FIXME: Change this later
app.config['SECRET_KEY'] = 'your_secret' # Replace with a secure key later on rn this is fine

# email configuration
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'a7e30523be428c'
app.config['MAIL_PASSWORD'] = '0313168bdde12f'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

#database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # or use PostgreSQL/MySQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# login manager setup
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    if int(user_id) == admin_user.id:
        return admin_user
    return None



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventory')
def inventory():
    
    return render_template('inventory.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    
    forum = ContactUsForum(csrf_enabled=False)

    if forum.validate_on_submit():
        name = forum.name.data
        email = forum.email.data
        phone = forum.phone.data
        message = forum.message.data
        
        # Here you would typically handle the form submission,
        # e.g., save to database or send an email.
        msg = Message('New Contact Us Message from {}'.format(name),sender=email, recipients = [f'myemail@email.com'])
        msg.body = f"""Name: {name} \nEmail: {email}\nPhone: {phone} 
        \nMessage: {message}"""
        try:
            mail.send(msg)
            flash("Message sent successfully!", "success")
            return redirect(url_for('contact'))  
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
        
    return render_template('contact.html', forum=forum)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    login_form = LoginForm(csrf_enabled=False)


    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        
        if username and check_password_hash(admin_user.password_hash, password):
            login_user(admin_user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('addInventory'))
        else:
            flash("Invalid username or password.", "danger")
            return render_template('index.html')
    return render_template('admin.html', form=login_form)


@app.route('/addInventory', methods=['GET', 'POST'])
def addInventory():

    form = VehicleForm(csrf_enabled=False)
    if form.validate_on_submit():
        make = form.make.data
        model = form.model.data
        year = form.year.data
        price = form.price.data
        image = form.image.data
        
        # Here you would typically handle the form submission,
        # e.g., save to database or send an email.
        
        flash("Vehicle added successfully!", "success")
        return redirect(url_for('addInventory'))

    return render_template('addInventory.html',  form=form)

if __name__ == '__main__':
    app.run(debug=True)