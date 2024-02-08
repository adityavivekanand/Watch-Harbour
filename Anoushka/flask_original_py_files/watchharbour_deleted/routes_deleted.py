import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from Project_flask import app, bcrypt, mail, db
from Project_flask.forms import (RegistrationForm, LoginForm, UpdateAccountForm ,RequestResetForm, ResetPasswordForm)
from Project_flask.models import User
from flask_login import login_user, current_user, logout_user, login_required
from passlib.hash import sha256_crypt

@app.route("/")
@app.route("/homepage")
def homepage():
    return render_template('homepage.html')

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('homepage'))
    form = RegistrationForm(request.form)
    if request.method == "POST":
        hashed_password = sha256_crypt.encrypt(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register2.html', title='Register', form=form)


# @app.route('/get_started', methods=['POST'])
# def get_started():
#     username = request.form.get('username')
#     return redirect(url_for('login_page', username=username))

# @app.route('/get_started/<username>', methods=['GET', 'POST'])
# def login_page(username):
#     # Render the login page with the pre-filled username
#     return render_template('login.html', username=username)



# @app.route('/get_started', methods=['GET', 'POST'])
# def get_started():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         return redirect(url_for('login_page'))
#     else:
#         # Handle GET request or display an initial form
#         return render_template('get_started.html')

# @app.route('/get_started/<username>', methods=['POST'])
# def login_page(username):
#     # If you're using the parameter from the URL, you can remove the line below
#     # username = request.form.get('username')
#     return render_template('login.html', username=username)

@app.route('/get_started', methods=['GET', 'POST'])
def get_started():
    if request.method == 'POST':
        username = request.form['username']
        return redirect(url_for('login_page', username=username))
    else:
        # Handle GET request or display an initial form
        return render_template('homepage.html')

@app.route('/get_started/<username>', methods=['GET','POST'])
def login_page(username):
    # If you're using the parameter from the URL, you can remove the line below
    # username = request.form.get('username')
    return render_template('loginnew.html', username=username)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and sha256_crypt.verify(password, user.password):
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('loginnew.html', title='Login')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))

# Add these later :

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


# def send_reset_email(user):
#     token = user.get_reset_token()
#     msg = Message('Password Reset Request',
#                   sender='noreply@demo.com',
#                   recipients=[user.email])
#     msg.body = f'''To reset your password, visit the following link:
# {url_for('reset_token', token=token, _external=True)}

# If you did not make this request then simply ignore this email and no changes will be made.
# '''
#     mail.send(msg)


# @app.route("/reset_password", methods=['GET', 'POST'])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('homepage'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('An email has been sent with instructions to reset your password.', 'info')
#         return redirect(url_for('login'))
#     return render_template('reset_request.html', title='Reset Password', form=form)


# @app.route("/reset_password/<token>", methods=['GET', 'POST'])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('homepage'))
#     user = User.verify_reset_token(token)
#     if user is None:
#         flash('That is an invalid or expired token', 'warning')
#         return redirect(url_for('reset_request'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user.password = hashed_password
#         db.session.commit()
#         flash('Your password has been updated! You are now able to log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('reset_token.html', title='Reset Password', form=form)