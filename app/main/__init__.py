from flask import Blueprint , jsonify , redirect , url_for  , request ,render_template
from app import session ,  rate , mp as users_data
from app.main.mp import getpage

main = Blueprint('main' , __name__  , static_folder='static')

@main.route('/', methods=['GET','POST'])
def index():
#     session['username'] = 'admin'
#     session['priv'] = 0
    # rec = rate.query.all()
    # print(rec)
    # for row in rec:
    #     print(row.id)
#     session.pop('username' ,None)
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