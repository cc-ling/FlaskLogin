from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField("账号", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()])
    submit = SubmitField("登录")


class RegisterForm(FlaskForm):
    username = StringField("账号")
    password = PasswordField("密码", validators=[DataRequired()])
    password2 = PasswordField(
        "确认密码", validators=[DataRequired(), EqualTo("password", message=u"密码必须相同")]
    )
    captcha = PasswordField("验证码", validators=[DataRequired()])
    submit = SubmitField("注册")
