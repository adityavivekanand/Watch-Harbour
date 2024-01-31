from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/homepage')
def home():
    return render_template('homepage.html')

if __name__ == 'main':
    app.run(debug=True)
