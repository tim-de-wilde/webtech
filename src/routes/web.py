from src import app, db
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from src.forms import LoginForm, RegisterForm
from src.models import User


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('home'))


    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Je bent al ingelogd')
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data) is not None:
            return redirect(url_for('register'))

        user = User(
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash('Je bent geregistreerd')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/')
@login_required
def home():
    return render_template('home.html')