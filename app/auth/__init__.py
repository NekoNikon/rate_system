from flask import Blueprint , request,  render_template , jsonify , redirect , url_for
from app import session , PH , mp
from app.database.smdb import DataManager


dm=DataManager()

auth_module = Blueprint('auth_module' , __name__ , template_folder='templates',static_folder='static')

@auth_module.route('/auth' , methods=['GET','POST'])
def auth():
    if request.method=='POST':
        d = {'auth':False}
        print('not auth')
        if 'username' in session:
            # response['is_login']=True
            return redirect(url_for('main.load_user' , user=session['username']), code=307)
        return  render_template('auth.html')

@auth_module.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        print(request.values)
        record = mp.query.filter_by(login=request.values['login']).first()
        print(record.hash)
        if PH.verify(record.hash , request.values['password']):
            session['username'] = request.values['login']
            session['priv'] = dm.GetManagePersonsPrivileges(session['username'])
    return redirect(url_for('main.load_user' ,  user=session['username'] ), code=307)

@auth_module.route('/logout', methods=['GET','POST'])
def logout():
    if request.method=='POST':
        session.pop('username', None)
        return redirect(url_for('main.index'), code=307)