from flask import Flask, request, render_template, Markup
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from datetime import datetime
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, TextAreaField,  BooleanField, PasswordField
from flask_wtf import FlaskForm
app = Flask(__name__)
from forms import ContactForm, LoginForm
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user



db = SQLAlchemy(app)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.debug = True
app.config['SECRET_KEY'] = 'a really really really really long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://flask_user:12345@localhost/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<{self.id}:{self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField()

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/')
def index():
    # links = []
    # links.append(Markup('<iframe width="560" height="315" src="https://www.youtube.com/embed/5qap5aO4i9A" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'))
    # links.append(Markup('<iframe src="https://player.vimeo.com/video/39880101" width="560" height="315" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>'))
    return render_template('index2.html')


@app.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/login/', methods=['post', 'get'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
    if user and user.check_password(form.password.data):
        login_user(user, remember=form.remember.data)
        return redirect(url_for('admin'))

    flash("Invalid username/password", 'error')
    return redirect(url_for('login'))
    return render_template('login.html', form=form)


if __name__ == '__main__':
    # u1 = User(name='vaasdsya', email = 'vas123@mail.ru', username = 'vaasdass');
    # u1.set_password('password')
    # db.session.add(u1)
    # db.session.commit()
    # print(u1.check_password('password'))
    print(db.session.query(User).all())
    manager.run()
