import joblib
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from website import db
from website.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from website.models import User
from website.ml.weather_data import WeatherData
from website.ml.crop_prediction import SimpleCropPrediction


main = Blueprint('main', __name__)

@main.route("/")
@main.route('/home')
def home():
    return render_template('home.html')

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.is_submitted():
        
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('User already exists!', 'danger')
            return render_template('register.html', title='Register', form=form)
        
        user = User(username=form.username.data, email = form.email.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
       
    return render_template('register.html', title='Register', form=form)


@main.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.is_submitted():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.password == form.password.data:
            login_user(user, remember= form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
            return render_template('login.html', title='Login', form = form)
        
    return render_template('login.html', title='Login', form = form)

@main.route("/logout")
def logout():
    logout_user()
    flash('User logged out successful!', 'success')
    return redirect(url_for('main.home'))

@main.route("/account")
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form = form)

@main.route("/result", methods=['GET'])
@login_required
def result():
    crop = request.args.get('crop')
    if not crop:
        return "No crop prediction found.", 400  
    return render_template('result.html', crop=crop)

@main.route('/predict', methods=['GET','POST'])
@login_required
def predict_crop():

    if request.method == 'POST':
        try:
            region = request.form['region']
            soil_type = request.form['soil_type']
            temperature = float(request.form['temperature'])
            weather_condition = request.form['weather_condition']

            # Load the encoders and model
            region_encoder = joblib.load('website/ml/region_label_encoder.pkl')
            soil_type_encoder = joblib.load('website/ml/soil_type_label_encoder.pkl')
            weather_condition_encoder = joblib.load('website/ml/weather_condition_label_encoder.pkl')
            crop_predictor = SimpleCropPrediction()

            # Encode inputs
            region_encoded = region_encoder.transform([region])[0]
            soil_encoded = soil_type_encoder.transform([soil_type])[0]
            weather_encoded = weather_condition_encoder.transform([weather_condition])[0]

            # Create the weather data object
            weather_data = WeatherData(region_encoded, soil_encoded, temperature, weather_encoded)

            # Predict crop
            predicted_crop = crop_predictor.predict_v2(weather_data)

            # Render the result
            return render_template('result.html', crop=predicted_crop)
        
        except KeyError as e:
            return f"Missing form field: {e}", 400
        except ValueError as ve:
            return f"Invalid input! {ve}", 400

    return render_template('prediction.html')