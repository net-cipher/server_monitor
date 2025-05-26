from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from db import log_stats
from monitor import get_system_stats

app = Flask(__name__, static_folder='static', template_folder='templates') 
CORS(app)

#Sqk database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/monitoring_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password: 
            session['user_id'] = user.id
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))

        flash("Invalid username or password", "danger")

    return render_template('login.html') 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose another.", "danger")
            return redirect(url_for('register'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful, please log in", "success")
        return redirect(url_for('login'))

    return render_template('register.html')  

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login')) 

    data = get_system_stats()  
    log_stats(data) 
    return render_template('dashboard.html', data=data) 

@app.route('/api/stats')
def stats():
    data = get_system_stats() 
    log_stats(data) 
    return jsonify(data)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login')) 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
