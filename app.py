from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Booking, Bus

app = Flask(__name__)
app.config['SECRET_KEY'] = 'swiftbus-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///swiftbus.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, email=email, phone=phone, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful! Welcome back!', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    total_bookings = len(bookings)
    confirmed_bookings = len([b for b in bookings if b.status == 'confirmed'])
    total_spent = sum([b.total_price for b in bookings])
    return render_template('dashboard.html',
                           bookings=bookings,
                           total_bookings=total_bookings,
                           confirmed_bookings=confirmed_bookings,
                           total_spent=total_spent)

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    total_users = User.query.count()
    total_bookings = Booking.query.count()
    total_buses = Bus.query.count()
    total_revenue = db.session.query(db.func.sum(Booking.total_price)).scalar() or 0
    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(10).all()
    return render_template('admin_dashboard.html',
                           total_users=total_users,
                           total_bookings=total_bookings,
                           total_buses=total_buses,
                           total_revenue=total_revenue,
                           recent_bookings=recent_bookings)

@app.route('/admin/buses')
@login_required
def manage_buses():
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    buses = Bus.query.all()
    return render_template('manage_buses.html', buses=buses)

@app.route('/admin/buses/add', methods=['GET', 'POST'])
@login_required
def add_bus():
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        bus = Bus(
            bus_name=request.form['bus_name'],
            bus_number=request.form['bus_number'],
            from_city=request.form['from_city'],
            to_city=request.form['to_city'],
            departure_time=request.form['departure_time'],
            arrival_time=request.form['arrival_time'],
            travel_date=request.form['travel_date'],
            total_seats=int(request.form['total_seats']),
            available_seats=int(request.form['total_seats']),
            price=float(request.form['price'])
        )
        db.session.add(bus)
        db.session.commit()
        flash('Bus added successfully!', 'success')
        return redirect(url_for('manage_buses'))
    return render_template('add_bus.html')

@app.route('/admin/buses/delete/<int:bus_id>')
@login_required
def delete_bus(bus_id):
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    bus = Bus.query.get_or_404(bus_id)
    db.session.delete(bus)
    db.session.commit()
    flash('Bus deleted successfully!', 'success')
    return redirect(url_for('manage_buses'))

@app.route('/admin/users')
@login_required
def manage_users():
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    users = User.query.all()
    return render_template('manage_users.html', users=users)

@app.route('/admin/bookings')
@login_required
def manage_bookings():
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard'))
    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    return render_template('manage_bookings.html', bookings=bookings)

@app.route('/search', methods=['POST'])
@login_required
def search():
    from_city = request.form['from_city']
    to_city = request.form['to_city']
    travel_date = request.form['travel_date']
    buses = Bus.query.filter_by(
        from_city=from_city,
        to_city=to_city,
        travel_date=travel_date
    ).all()
    return render_template('search_results.html',
                           buses=buses,
                           from_city=from_city,
                           to_city=to_city,
                           travel_date=travel_date)

@app.route('/book/<int:bus_id>', methods=['GET', 'POST'])
@login_required
def book_ticket(bus_id):
    bus = Bus.query.get_or_404(bus_id)
    if request.method == 'POST':
        seats = int(request.form['seats'])
        if seats > bus.available_seats:
            flash('Not enough seats available!', 'danger')
            return redirect(url_for('book_ticket', bus_id=bus_id))
        total_price = seats * bus.price
        booking = Booking(
            user_id=current_user.id,
            bus_id=bus.id,
            seats_booked=seats,
            total_price=total_price
        )
        bus.available_seats -= seats
        db.session.add(booking)
        db.session.commit()
        flash('Ticket booked successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('book_ticket.html', bus=bus)

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True)
