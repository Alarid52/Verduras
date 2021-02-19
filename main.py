from flask import Flask, request, make_response, redirect, render_template, url_for, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField, validators

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['WTF_CSRF_ENABLED']=False
app.config['SECRET_KEY'] = 'no_hay'

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', [validators.Length(min=4, max=25)])
    password = PasswordField('Contraseña',[validators.DataRequired()])
    submit = SubmitField('Enviar')

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', [validators.Length(min=4, max=25)])
    email = StringField('Correo electronico', [validators.Length(min=6, max=35)])
    password = PasswordField('Contraseña', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirmar contraseña')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    submit = SubmitField('Registrar')


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/registro', methods=['GET','POST'])
def registro():
    reg_form = RegistrationForm()
    context = {
        "reg_form":reg_form
    }
    return render_template('registro.html',**context)

@app.route('/login', methods=['GET','POST'])
def login():
    log_form = LoginForm()
    context = {
        "log_form":log_form
    }
    if log_form.validate_on_submit():
        username = log_form.username.data
        password = log_form.password.data
        session['username'] = username
        session['password'] = password
        response = make_response(redirect('/user'))
        return response
    return render_template("login.html",**context)

@app.route('/user')
def usuario():
    return render_template("user.html")