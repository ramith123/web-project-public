from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, EqualTo, Length, Regexp


class Register(FlaskForm):
    username = StringField("username", validators=[InputRequired()])
    # email = StringField('email', validators=[Email(), InputRequired()])
    password = PasswordField(
        "Password",
        validators=[
            Length(
                min=8, max=50, message="Password must be between 8 and 50 characters.",
            ),
            InputRequired(),
            EqualTo("confirm", message="Passwords must match."),
            Regexp(
                "^(?=.{8,})(?=.*[a-z])(?=.*[A-Z]).*$",
                message="Must contain at least 1 UpperCase, 1 lowerCase.",
            ),
        ],
    )
    confirm = PasswordField("Repeat password", validators=[InputRequired()])
    accept_tos = BooleanField(
        'I accept the <a href="#tos">Terms of Service</a> and the <a href="#priv"> Privacy Policy</a>',
        validators=[InputRequired()],
        render_kw={"class": "filled-in"},
    )
    submit = SubmitField(
        "Register",
        render_kw={"class": "btn waves-effect waves-light amber darken-3 white-text"},
    )


class Login(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField(
        "Next",
        render_kw={"class": "btn waves-effect waves-light white-text amber darken-3"},
    )