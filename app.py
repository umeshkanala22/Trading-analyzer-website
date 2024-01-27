from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from utils.data import stock_names
from utils.get_data import get_stock_data, get_live_stock_data

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

# Initialize Database within Application Context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/test')
def test():
    stocks = stock_names
    return render_template('dashboard.html', stocks=stocks)

@app.route('/plot')
def plot():
    stocks = stock_names
    return render_template('plot.html', stocks=stocks)

# apis

@app.route('/api/stock', methods=['GET'])
def get_stock_data_api():
    selected_stock = request.args.get('stock')
    data = get_live_stock_data(selected_stock)
    return data

@app.route('/api/plot', methods=['GET'])
def get_plot():
    selected_stock = request.args.get('stock')
    selected_criteria = request.args.get('criteria')
    start_date = request.args.get('begin')
    end_date = request.args.get('end')
    # replace '-' with ',' in start_date and end_date
    start = start_date.replace('-', ',')
    end = end_date.replace('-', ',')
    print("start_date: ", start)
    image_path = get_stock_data(selected_stock, start, end, selected_criteria)
    return image_path


if __name__ == '__main__':
    app.run(debug=True)
