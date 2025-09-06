
from flask import Flask, jsonify, request, redirect, url_for, flash, Response
from flask import render_template
from forms import ContactUsForum, VehicleForm, LoginForm
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models import User, Vehicle, admin_user
# these are for the image handling 
from werkzeug.utils import secure_filename
import os


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

# image handling setup
UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # or use PostgreSQL/MySQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
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
    cars = Vehicle.query.all()
    for car in cars:
        print(f"this is IN CAR {car}")
    return render_template('inventory.html', cars = cars)

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
@login_required
def addInventory():
    form = VehicleForm(csrf_enabled=False)

    if form.validate_on_submit():
        image_file = form.image.data
        filename = secure_filename(image_file.filename)

        # Save image to disk
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)

        car = Vehicle(
            make=form.make.data,
            model=form.model.data,
            year=int(form.year.data),
            price=float(form.price.data),
            kilometers=form.kilometers.data,
            image_filename=filename
        )
        db.session.add(car)
        db.session.commit()

        flash("Vehicle added successfully!", "success")
        return redirect(url_for('addInventory'))

    return render_template('addInventory.html', form=form)


@app.route('/vehicle_image/<int:vehicle_id>')
def vehicle_image(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return Response(vehicle.image, mimetype=vehicle.image_mimetype)


if __name__ == '__main__':
    app.run(debug=True)