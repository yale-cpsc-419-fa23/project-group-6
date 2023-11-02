from flask import Blueprint, render_template, session, flash, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/home')
def home():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('home.html')
