from flask import Flask, render_template, redirect, url_for, request, flash
from forms import LoginForm, RegistrationForm, ResetPasswordForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a1ee053b3ecd877a93c9565a5bab40b1a533e666d5ce30b8b941ef88354766f0'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

@app.route('/')
@app.route('/homepagepage')
def homepagepage():
    return render_template('homepagepage.html')

# log in karne ke baad dashboard redirect karenge and register ke baad login
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/get_started', methods=['POST'])
def get_started():
    username = request.form.get('username')
    return redirect(url_for('login_page', username=username)) 

@app.route('/get_started/<username>')
def login_page(username):
    # Render the login page with the pre-filled username
    return render_template('login.html', username=username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# @app.route('/forgot_password')
# def forgot_password():
#     return render_template('forgot_password.html')
@app.route("/reset_password", methods=['GET', 'POST'])
def forgot_password():
#     if current_user.is_authenticated:
#         return redirect(url_for('homepage'))
#     user = User.verify_reset_token(token)
#     if user is None:
#         flash('That is an invalid or expired token', 'warning')
#         return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    # if form.validate_on_submit():
    #     hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    #     user.password = hashed_password
    #     db.session.commit()
    #     flash('Your password has been updated! You are now able to log in', 'success')
    #     return redirect(url_for('login'))
    return render_template('forgot_password.html', title='Reset Password', form=form)

@app.route('/logout')
def logout():
    return redirect('login.html')

if __name__ == '__main__':
    app.run(debug=True)

