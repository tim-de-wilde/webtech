from src import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from src.forms import LoginForm, RegisterForm, ActorForm, DeleteForm
from src.models import User, Actor
from src.api.ActorApi import ActorApi


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
        if User.query.filter_by(email=form.email.data).first() is not None:
            form.email.errors.append('This e-mail address is already in use.')
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def home():
    return render_template('home.html')


@app.route('/actors')
@login_required
def index_actors():
    return render_template('actors/index.html', actors=ActorApi.index())


@app.route('/actors/create', methods=['GET', 'POST'])
@login_required
def create_actor():
    form = ActorForm()

    if form.validate_on_submit():
        ActorApi.create(form)
        flash('Acteur aangemaakt!')
        return redirect(url_for('index_actors'))

    return render_template('actors/create_edit.html', form=form, updating=False)


@app.route('/actors/<int:actor_id>')
@login_required
def show_actor(actor_id):
    return render_template('actors/show.html', actor=ActorApi.index_one(actor_id))


@app.route('/actors/<int:actor_id>/edit', methods=['GET', 'POST'])
@login_required
def update_actor(actor_id):
    form = ActorForm()

    if form.validate_on_submit():
        ActorApi.update(actor_id, form)
        flash('Acteur aangepast!')
        return redirect(url_for('index_actors'))

    return render_template('actors/create_edit.html', form=form, updating=True, actor=ActorApi.index_one(actor_id))


@app.route('/actors/<int:actor_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_actor(actor_id):
    form = DeleteForm()

    if form.validate_on_submit():
        ActorApi.delete(form.id.data)
        flash('Acteur verwijderd.')
        return redirect(url_for('index_actors'))

    return render_template('actors/confirm_delete.html', actor=ActorApi.index_one(actor_id), form=form)
