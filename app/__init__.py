from flask import Flask, request, current_app , session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from argon2 import PasswordHasher


app = Flask(__name__)
app.secret_key='SHH'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin_rate:jojo1234@localhost:5432/rate_system'
data_app = SQLAlchemy(app)
PH = PasswordHasher(hash_len=100, salt_len=100)

class rate(data_app.Model):
    id = data_app.Column('rate_id' , data_app.Integer, primary_key=True)
    value = data_app.Column('rate_value', data_app.Float, nullable=False)
    season_id = data_app.Column('rate_season_id', data_app.Integer, data_app.ForeignKey('season.id'), nullable=False)
    teacher_id = data_app.Column('rate_teacher_id' , data_app.Integer, data_app.ForeignKey('teachers_id'), nullable=False)
    indicator_id = data_app.Column('rate_indicator_id' , data_app.Integer, data_app.ForeignKey('indicator.id'), nullable=False)
    def __init__(self , value , season, teacher, indicator):
        self.value=value
        self.season=season
        self.teacher=teacher
        self.indicator=indicator

class season(data_app.Model):
    id = data_app.Column('season_id', data_app.Integer, primary_key=True)
    date = data_app.Column('season_date' , data_app.DateTime, nullable=False)
    # sr = data_app.relationship('rate' , backref='season',lazy=True)
    def __init__(self , date):
        self.date = date

class indicator(data_app.Model):
    id = data_app.Column('indicator_id',data_app.Integer, primary_key=True)
    name = data_app.Column('indicator_name',data_app.String(100), nullable=False)
    group = data_app.Column('indicator_group_id', data_app.Integer , data_app.ForeignKey('group_indicator.id'), nullable=False)
    # ir = data_app.relationship('rate' , backref='indicator',lazy=True)
    # gi = data_app.relationship('rate' , backref='group_indicator',lazy=True)
class group_indicator(data_app.Model):
    id = data_app.Column(data_app.Integer, primary_key=True)
    name = data_app.Column(data_app.String(100), nullable=False)

class teachers(data_app.Model):
    __tablename__ = 'teachers'
    id = data_app.Column('teachers_id', data_app.Integer, primary_key=True)
    code = data_app.Column('teachers_iin', data_app.String(4), unique=True, nullable=False)
    s_name = data_app.Column('teachers_second_name', data_app.String, nullable=False)
    f_name = data_app.Column('teachers_first_name' , data_app.String, nullable=False)
    t_name = data_app.Column('teachers_third_name' , data_app.String, nullable=False)
    # tr = data_app.relationship('rate' , backref='teachers',lazy=True)
    # group = data_app.Column('teachers_group', data_app.Integer, data_app.ForeignKey('group_teacher.id'), nullable=False)

class group_teacher(data_app.Model):
    id = data_app.Column(data_app.Integer, primary_key=True)
    spec = data_app.Column(data_app.String(100), nullable=False)

class mp(data_app.Model):
    __tablename__ = 'manage_persons'
    id = data_app.Column('manage_persons_id', data_app.Integer, primary_key=True)
    login = data_app.Column('manage_persons_login',data_app.String(50), unique=True, nullable=False)
    hash = data_app.Column('manage_persons_password',data_app.String, nullable=False)
    priv = data_app.Column('manage_persons_priv_value', data_app.Integer, nullable=False)
    name = data_app.Column('manage_persons_name' , data_app.String , nullable=False)

from app.main import main as main_bp
app.register_blueprint(main_bp , url_prefix='/')

from app.auth import auth_module as auth_bp
app.register_blueprint(auth_bp ,  url_prefix='/')

from app.rate import rate_module as rate_bp
app.register_blueprint(rate_bp , url_prefix='/')

from app.database import data_module as data_bp
app.register_blueprint(data_bp)

from app.indicators import ind_module as ind_bp
app.register_blueprint(ind_bp, url_prefix='/')

from app.MP import users_module as us_bp
app.register_blueprint(us_bp , url_prefix='/')