from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,  Length, Regexp
# from models import Vehicle

class ContactUsForum(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[
        Length(min=7, max=20, message="Please enter a valid phone number."),
        Regexp(r'^[\d\-\+\(\) ]+$', message="Invalid phone number format.")
    ])
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')

class VehicleForm(FlaskForm):
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    kilometers = StringField('Kilometers', validators=[DataRequired()])
    image = FileField('Vehicle Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    
    submit = SubmitField('Add Vehicle')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SortVheiclesForm(FlaskForm):
    sort_by = SelectField('Sort By', choices=[('', '-- Select --'),
                                            ('price_asc', 'Price (Low to High)'), 
                                           ('price_dec', 'Price (High to Low)'),
                                            ('year_asc', 'Year (Old to New)'),
                                            ('year_dec', 'Year (New to Old)'),
                                            ('km_asc', 'Kilometers (Low to High)'),
                                            ('km_dec', 'Kilometers (High to Low)')])
    submit = SubmitField('Sort')