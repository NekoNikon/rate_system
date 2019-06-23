from flask import Blueprint , render_template ,request ,jsonify
from app.database.smdb import DataManager
from app import teachers ,mp, data_app
import random
from argon2 import PasswordHasher 
from argon2.exceptions import VerificationError

ph = PasswordHasher(hash_len=100)

dm = DataManager()
users_module = Blueprint('MP' ,__name__)

@users_module.route('/user_edit' , methods=['GET' , 'POST'])
def user_edit():
    if request.method=='POST':
        records = dm.GetMP()
        print(records)
        return render_template('user_list.html', records=records)

@users_module.route('/edit_pass', methods=['GET','POST'])
def edit_pass():
    data = request.values
    User = mp.query.get(int(data['id']))
    print(User.login)
    try:
        if ph.verify(User.hash , data['old']):
            User.hash = ph.hash(data['new'])
            data_app.session.commit()
    except VerificationError as identifier:
        return jsonify({'edit':False})
    return jsonify({'edit':True})

@users_module.route('/edit_user' , methods=['GET','POST'])
def edit_user():
    data= request.values
    dm.EditUser(data['login'], data['name'] , int(data['id']))
    return jsonify({'edit':True})

@users_module.route('/add_user' , methods=['GET','POST'])
def add_user():
    if request.method=='POST':
        data = request.values
        dm.AddUser(data['login'],data['password'] , data['priv'] , data['name'])
        d = { 
            'add':True
        }
        return jsonify(d)


    

@users_module.route('/del_user' ,methods=['GET','POST'])
def del_user():
    if request.method=='POST':
        data = request.values['id']
        dm.DelUser(int(data))
    d = {'d':True}
    return jsonify(d)

@users_module.route('/load_teacher' , methods=['GET','POST'])
def load_teacher():
    teacher_list = teachers.query.all()
    return render_template('list_teachers.html' , teachers=teacher_list)

@users_module.route('/add_head', methods=['GET','POST'])
def add_head():
    code = ''
    for i in range(4):
        code += str(int(round(random.random(),1)*10)) 
    # print(int(round(random.random(),1)*10))
    print(code)
    data = request.values
    dm.AddHead(data['sname'] , data['fname'], data['tname'], data['tg'] ,code)
    return jsonify({'add':True})

@users_module.route('/add_teacher', methods=['GET','POST'])
def add_teacher():
    code = ''
    for i in range(4):
        code += str(int(round(random.random(),1)*10)) 
    # print(int(round(random.random(),1)*10))
    print(code)
    data = request.values
    dm.AddTeacher(data['sname'] , data['fname'], data['tname'], code)
    return jsonify({'add':True})

@users_module.route('/edit_teacher' , methods=['GET','POST'])
def edit_teacher():
    data = request.values
    print(data)
    dm.EditTeacher(int(data['id']), data['sn'] , data['fn'] , data['tn'], data['code'])
    return jsonify({'edit':True})

@users_module.route('/del_teacher' , methods=['GET','POST'])
def del_teacher():
    dm.DelTeacher(int(request.values['id']))
    return jsonify({'del':True})