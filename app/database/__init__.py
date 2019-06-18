from flask import Blueprint
# from flask_sqlalchemy import SQLAlchemy

data_module = Blueprint('database', __name__)
# data_module.config['SQLALCHEMY_daTABASE_URL']='postgres://postgres:123@localhost/RS'
# RS = SQLAlchemy(data_module)

from app.database import smdb