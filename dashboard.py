# Simple Flask dashboard with login (admin: dahassistantsai)

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your-secret-key'

ADMIN_USERNAME = 'dahassistantsai'
ADMIN_PASSWORD = 'supersecurepassword'  # Change this!

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session and session['username'] == ADMIN_USERNAME:
        return render_template('dashboard.html', user=ADMIN_USERNAME)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)