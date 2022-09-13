from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo

class RegisterForm(FlaskForm):
    userid = StringField('id', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('pw', validators=[DataRequired(), EqualTo('password_2')]) #비밀번호 확인
    password_2 = PasswordField('pw_2', validators=[DataRequired()])
    phone = PasswordField('phone', validators=[DataRequired()])