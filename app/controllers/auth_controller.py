from flask import Blueprint, render_template, redirect, url_for, flash, session

from app.models.user import User
from app.views.forms import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(form.email.data)
        if user and user.check_password(form.password.data):
            session['user_id'] = user.userId
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.home'))
        flash('Invalid username or password.', 'danger')
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f'{err}', 'danger')
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create the user
        try:
            User.create(username=form.username.data, password=form.password.data,
                        email=form.email.data, gender=None, birthday=None)
            flash('Registration successful!', 'success')
            return redirect(url_for('auth.login'))
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template('register.html', form=form)
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f'{err}', 'danger')

    return render_template('register.html', form=form)


@auth.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    return redirect(url_for('auth.login'))
