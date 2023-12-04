from flask import Blueprint, request, render_template, redirect, flash, url_for, session
from datetime import datetime

from app.models.user import User
from app.views.forms import SettingsForm

settings = Blueprint('settings', __name__)


@settings.context_processor
def inject_datetime():
    return {'datetime': datetime}


@settings.route('/settings', methods=['GET', 'POST'])
def user_settings():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user = User.find_by_id(user_id)
    form = SettingsForm(obj=user)

    if request.method == 'GET':
        form.username.data = user.get_username()
        form.gender.data = user.get_gender()
        form.birthday.data = user.get_birthday()
    elif form.validate_on_submit():
        user.update_username(form.username.data)
        user.update_gender(form.gender.data)

        if form.birthday.data:
            user.update_birthday(form.birthday.data)

        if form.new_password.data:
            user.update_password(form.new_password.data)

        flash('Your settings have been updated.', 'success')
        return redirect(url_for('settings.user_settings'))
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f'{err}', 'danger')

    return render_template('settings.html', form=form, user=user)
