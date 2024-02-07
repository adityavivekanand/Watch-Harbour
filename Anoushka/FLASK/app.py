from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

#@app.route('/')
# @app.route('/homepage')
# def homepage():
#     return render_template('homepage.html')

@app.route('/')
def dashboard():
     return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/get_started', methods=['POST'])
def get_started():
    username = request.form.get('username')
    return redirect(url_for('login_page', username=username))

@app.route('/get_started/<username>')
def login_page(username):
    # Render the login page with the pre-filled username
    return render_template('login.html', username=username)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    return redirect('login.html')

if __name__ == '__main__':
    app.run(debug=True)

# log in karne ke baad dashboard redirect karenge and register ke baad login
# def dashboard():
#     return render_template('dashboard.html')