from flask import Blueprint , jsonify , redirect , url_for  , request ,render_template
from app import session , season, data_app, rate , mp as users_data 
from app.main.mp import getpage
from datetime import datetime , date 
from app.rate import add_seaon

main = Blueprint('main' , __name__  , static_folder='static')

@main.route('/', methods=['GET','POST'])
def index():
    last = season.query.order_by(season.date.desc()).first()
    print(last.date.month)
    now = date.today()
    
    print(now.month)
    if now == last.date:
        print('семестр существует')
    elif now.month == 6 or now.month == 1:
        if now.day == 30:
            add_seaon()

    response = { 'is_login': False }
    if request.method=='POST':
        if 'username' in session:
            response['is_login']=True
            redirect(url_for('main.load_user' , user=session['username']), code=307)
    return render_template('index.html')

@main.route('/check', methods=['GET' , 'POST'])
def check():
    d = {'session':False}
    if request.method=='POST':
        if 'username' in session:
            d['session']= True
    return jsonify(d)
            # return redirect(url_for('main.load_side'),code=307)

@main.route('/guest' , methods=['GET','POST'])
def guest():
    if request.method=='POST':
        return render_template('guest.html')

@main.route('/load_user/<user>', methods=['GET' , 'POST'])
def load_user(user):
    name = users_data.query.filter_by(login=user).first()
    print(name)
    return '''<h1>Пользователь - %s</h1>''' % name.name


@main.route('/load_side' , methods=['GET','POST'])
def load_side():
    if request.method=='POST':
        return render_template(getpage(session['priv']))