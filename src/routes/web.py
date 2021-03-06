from src import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from src.forms import LoginForm, RegisterForm, ActorForm, DeleteForm, DirectorForm, RoleForm, FilmForm, CommentForm
from src.models import User, Actor, Film
from src.api.ActorApi import ActorApi
from src.api.DirectorApi import DirectorApi
from src.api.RoleApi import RoleApi
from src.api.FilmApi import FilmApi


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def redirect_to_films():
    return redirect(url_for('index_films'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('index_films'))


    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Je bent al ingelogd')
        return redirect(url_for('index_films'))

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
    return redirect(url_for('index_films'))


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


@app.route('/directors')
@login_required
def index_directors():
    return render_template('directors/index.html', directors=DirectorApi.index())


@app.route('/directors/create', methods=['GET', 'POST'])
@login_required
def create_director():
    form = DirectorForm()

    if form.validate_on_submit():
        DirectorApi.create(form)
        flash('Regisseur aangemaakt!')
        return redirect(url_for('index_directors'))

    return render_template('directors/create_edit.html', form=form, updating=False)


@app.route('/directors/<int:director_id>')
@login_required
def show_director(director_id):
    return render_template('directors/show.html', director=DirectorApi.index_one(director_id))


@app.route('/directors/<int:director_id>/edit', methods=['GET', 'POST'])
@login_required
def update_director(director_id):
    form = DirectorForm()

    if form.validate_on_submit():
        DirectorApi.update(director_id, form)
        flash('Regisseur aangepast!')
        return redirect(url_for('index_directors'))

    return render_template('directors/create_edit.html', form=form, updating=True, director=DirectorApi.index_one(director_id))


@app.route('/directors/<int:director_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_director(director_id):
    form = DeleteForm()

    if form.validate_on_submit():
        DirectorApi.delete(form.id.data)
        flash('Regisseur verwijderd.')
        return redirect(url_for('index_directors'))

    return render_template('directors/confirm_delete.html', director=DirectorApi.index_one(director_id), form=form)


@app.route('/roles')
@login_required
def index_roles():
    return render_template('roles/index.html', roles=RoleApi.index())


@app.route('/roles/create', methods=['GET', 'POST'])
@login_required
def create_role():
    form = RoleForm()

    if form.validate_on_submit():
        RoleApi.create(form)
        flash('Rol aangemaakt!')
        return redirect(url_for('index_roles'))

    return render_template('roles/create_edit.html', form=form, updating=False, actors=ActorApi.index(), films=FilmApi.index())


@app.route('/roles/<int:role_id>')
@login_required
def show_role(role_id):
    return render_template('roles/show.html', role=RoleApi.index_one(role_id))


@app.route('/roles/<int:role_id>/edit', methods=['GET', 'POST'])
@login_required
def update_role(role_id):
    form = RoleForm()

    if form.validate_on_submit():
        RoleApi.update(role_id, form)
        flash('Rol aangepast!')
        return redirect(url_for('index_roles'))

    return render_template('roles/create_edit.html', form=form, updating=True, role=RoleApi.index_one(role_id), actors=ActorApi.index(), films=FilmApi.index())


@app.route('/roles/<int:role_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_role(role_id):
    form = DeleteForm()

    if form.validate_on_submit():
        RoleApi.delete(form.id.data)
        flash('Rol verwijderd.')
        return redirect(url_for('index_roles'))

    return render_template('roles/confirm_delete.html', role=RoleApi.index_one(role_id), form=form)


@app.route('/films')
def index_films():
    return render_template('films/index.html', films=FilmApi.index())


@app.route('/films/create', methods=['GET', 'POST'])
@login_required
def create_film():
    form = FilmForm()

    if form.validate_on_submit():
        FilmApi.create(form)
        flash('Film aangemaakt!')
        return redirect(url_for('index_films'))

    return render_template('films/create_edit.html', form=form, updating=False, directors=DirectorApi.index())


@app.route('/films/<int:film_id>', methods=['GET', 'POST'])
def show_film(film_id):
    form = CommentForm()

    if current_user.is_authenticated and form.validate_on_submit():
        FilmApi.create_comment(film_id, current_user.id, form)

    return render_template('films/show.html', film=FilmApi.index_one(film_id), form=form)


@app.route('/films/<int:film_id>/edit', methods=['GET', 'POST'])
@login_required
def update_film(film_id):
    form = FilmForm()

    if form.validate_on_submit():
        FilmApi.update(film_id, form)
        flash('Film aangepast!')
        return redirect(url_for('index_films'))

    return render_template('films/create_edit.html', form=form, updating=True, film=FilmApi.index_one(film_id), directors=DirectorApi.index())


@app.route('/films/<int:film_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_film(film_id):
    form = DeleteForm()

    if form.validate_on_submit():
        FilmApi.delete(form.id.data)
        flash('Film verwijderd.')
        return redirect(url_for('index_films'))

    return render_template('films/confirm_delete.html', film=FilmApi.index_one(film_id), form=form)