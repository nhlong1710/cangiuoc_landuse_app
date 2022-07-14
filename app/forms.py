from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, InputRequired
from app.models import User


class signUpForm(FlaskForm):
    account = StringField('Account', validators=[DataRequired(), Length(min=5, message=('Your id is too short.'))])
    fullName = StringField('Full Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message=('Your password is too short.'))])
    rePassword = PasswordField('reType Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_passengerId(self, account):
        account = User.query.filter_by(account=account.data).first()
        if account is not None:
            raise ValidationError('username has been already used! Please use a different username.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('email has been already used! Please use a different email.')


class loginForm(FlaskForm):
    account = StringField('Account', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class InsertNewParcelForm(FlaskForm):
    owner = StringField('Chủ sở hữu', validators=[DataRequired()])
    address = StringField('Địa chỉ')
    ward = SelectField('Xã/Thị Trấn', validators=[DataRequired()])
    area = StringField('Diện tích', validators=[DataRequired()])
    land_use = StringField('Mục đích sử dụng đất', validators=[DataRequired()])
    geom = StringField('Tọa độ thửa đất', validators=[DataRequired()])
    submit = SubmitField('Thêm')


class EditParcelForm(FlaskForm):
    owner = StringField('Chủ sở hữu', validators=[DataRequired()])
    address = StringField('Địa chỉ', validators=[DataRequired()])
    ward = SelectField('Xã/Thị Trấn')
    area = StringField('Diện tích', validators=[DataRequired()])
    land_use = StringField('Mục đích sử dụng đất', validators=[DataRequired()])
    updated_year = StringField('Ngày cập nhật thông tin', validators=[DataRequired()])
    submit = SubmitField('Sửa')
