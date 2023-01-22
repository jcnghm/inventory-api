from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from app.forms import UserLoginForm
from app.models import User, db
from helpers import is_valid_password

#  Imports for Flask Login
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            # Get form variables
            email = form.email.data
            password = form.password.data
            name = form.name.data
            confirm_password = form.confirm_password.data

            # Validate password
            if is_valid_password(password, confirm_password) is False:
                raise Exception(
                    'Invalid Form Data: Password fields do not meet criteria.'
                )

            user = User(name, email, password=password)

            db.session.add(user)
            db.session.commit()

    except:
        raise Exception('Invalid Form Data: Please Check Your Form')


@auth.route('/signin', methods=['GET', 'POST'])
def signin():

    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in', 'auth-success')
                return redirect(url_for('site.profile'))

            else:
                flash('Your Email/Password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')
    return render_template('signin.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))
