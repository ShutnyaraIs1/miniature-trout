from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from accounts import accounts
from forms import LoginForm, CharacterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LbCKkDTd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///characters.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите, чтобы получить доступ к этой странице.'
login_manager.login_message_category = 'info'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    orientation = db.Column(db.String(50), nullable=False)
    race = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    personality = db.Column(db.Text, nullable=False)
    strengths = db.Column(db.Text, nullable=False)
    weaknesses = db.Column(db.Text, nullable=False)
    art = db.Column(db.Text, nullable=False)
    class_type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()
    for username, password in accounts.items():
        if not User.query.filter_by(username=username).first():
            db.session.add(User(username=username, password=generate_password_hash(password), role='Ankietolog'))
    db.session.commit()

@app.route('/')
def home():
    return redirect(url_for('characters'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('characters'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('characters'))

@app.route('/characters')
def characters():
    characters = Character.query.all()
    return render_template('characters.html', characters=characters)

@app.route('/character/<int:character_id>')
def character(character_id):
    character = Character.query.get_or_404(character_id)
    return render_template('character.html', character=character)

@app.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if current_user.role != 'Ankietolog':
        flash('Access denied.')
        return redirect(url_for('characters'))
    form = CharacterForm()
    if form.validate_on_submit():
        character = Character(
            name=form.name.data,
            nickname=form.nickname.data,
            status=form.status.data,
            gender=form.gender.data,
            orientation=form.orientation.data,
            race=form.race.data,
            bio=form.bio.data,
            personality=form.personality.data,
            strengths=form.strengths.data,
            weaknesses=form.weaknesses.data,
            art=form.art.data,
            class_type=form.class_type.data,
            location=form.location.data
        )
        db.session.add(character)
        db.session.commit()
        return redirect(url_for('characters'))
    return render_template('create.html', form=form)

@app.route('/edit/<int:character_id>', methods=('GET', 'POST'))
@login_required
def edit(character_id):
    if current_user.role != 'Ankietolog':
        flash('Access denied.')
        return redirect(url_for('characters'))
    character = Character.query.get_or_404(character_id)
    form = CharacterForm(obj=character)
    if form.validate_on_submit():
        form.populate_obj(character)
        db.session.commit()
        return redirect(url_for('characters'))
    return render_template('create.html', form=form, character=character)

if __name__ == '__main__':
    app.run(debug=True)