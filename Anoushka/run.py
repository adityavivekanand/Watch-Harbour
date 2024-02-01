from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/homepage')
def home():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

if __name__ == 'main':
    app.run(debug=True)
