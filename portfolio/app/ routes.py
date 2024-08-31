# app/routes.py

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from app.models import User, Portfolio, SignUpRequest
from app.forms import LoginForm, SignUpForm, PortfolioForm
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def home():
    return render_template('guest_view.html', title='Home')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('student_dashboard'))
    form = SignUpForm()
    if form.validate_on_submit():
        signup_request = SignUpRequest(student_name=form.username.data, email=form.email.data)
        db.session.add(signup_request)
        db.session.commit()
        flash('Your sign-up request has been submitted!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('student_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    return render_template('student_dashboard.html', title='Student Dashboard')

@app.route('/create_portfolio', methods=['GET', 'POST'])
@login_required
def create_portfolio():
    form = PortfolioForm()
    if form.validate_on_submit():
        portfolio = Portfolio(youtube_link=form.youtube_link.data, description=form.description.data, relevant_links=form.relevant_links.data, author=current_user)
        db.session.add(portfolio)
        db.session.commit()
        flash('Your portfolio has been created!', 'success')
        return redirect(url_for('student_dashboard'))
    return render_template('create_portfolio.html', title='Create Portfolio', form=form)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('student_dashboard'))
    signup_requests = SignUpRequest.query.filter_by(status='Pending').all()
    return render_template('admin_dashboard.html', title='Admin Dashboard', signup_requests=signup_requests)

@app.route('/approve_request/<int:request_id>')
@login_required
def approve_request(request_id):
    if not current_user.is_admin:
        return redirect(url_for('student_dashboard'))
    signup_request = SignUpRequest.query.get_or_404(request_id)
    new_user = User(username=signup_request.student_name, email=signup_request.email, password_hash=generate_password_hash('defaultpassword', method='sha256'))
    db.session.add(new_user)
    signup_request.status = 'Approved'
    db.session.commit()
    flash('Signup request approved!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/reject_request/<int:request_id>')
@login_required
def reject_request(request_id):
    if not current_user.is_admin:
        return redirect(url_for('student_dashboard'))
    signup_request = SignUpRequest.query.get_or_404(request_id)
    signup_request.status = 'Rejected'
    db.session.commit()
    flash('Signup request rejected!', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
