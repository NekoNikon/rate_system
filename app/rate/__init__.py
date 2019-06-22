from flask import Blueprint  , render_template, jsonify , json
from app import  mp , teachers , request , rate , indicator,season
from app.database.smdb import DataManager

dm = DataManager()

rate_module = Blueprint('rate_module' ,__name__ )

@rate_module.route('/pre_view_rate', methods=['GET','POST'])
def pre_view_rate():
    count = dm.GetSeasonsId()
    return render_template('rate_tables.html' , count=count)


@rate_module.route('/view_rate', methods=['GET' , 'POST'])
def view_rate():
    if request.method=='POST':
        ret = {}
        teacher = teachers.query.filter_by(code=request.values['code']).first()
        data = rate.query.filter_by(teacher_id=teacher.id)
        i = dm.GetTeacherRateByIin(request.values['code'])
        res = dm.GetRateByTeacher(int(teacher.id))
        rates = dm.GetRateByTeacher(teacher.id)
        inds = dm.GetInds()
        seasons = dm.GetSeasonsId()
        # inds = indicator.query.join(rate , rate.indicator_id==indicator.id)
        ret['teacher'] = '%s %s %s' % (teacher.s_name , teacher.f_name , teacher.t_name) 
        ret['teacher_id'] = teacher.id
        ret['seasons'] = seasons
        ret['inds'] = inds
        ret['res'] = res
        # for row in inds:
        #     pass
        f ={'a':1} 
        return jsonify(ret)
        # return render_template('result.html' , records=teacher , values=val , inds=inds , seasons=seasons)

@rate_module.route('/get_json_rate' , methods=['GET','POST'])
def get_json_rate():
    if request.method=='POST':
        return 

@rate_module.route('/edit_rate_page', methods=['GET', 'POST'])
def edit_rate_page():
    if request.method=='POST':
        teacher_list = teachers.query.all()
        return render_template('edit_rate_page.html', teachers=teacher_list)

@rate_module.route('/preloadrates' , methods=['GET','POST'])
def preloadrates():
    if request.method=='POST':
        count = dm.GetSeasonsId()
        return render_template('rate_tables.html' , count=count)

@rate_module.route('/load_rates' , methods=['GET' , 'POST'])
def load_rates():
    if request.method=='POST':
        teacher = teachers.query.filter_by(id=request.values['id']).first()
        seasons = dm.GetSeasonsId()
        code = request.values['id']
        inds = dm.GetInds()
        res = dm.GetRateByTeacher(int(code))
        ret = {}
        ret['teacher'] = '%s %s %s' % (teacher.s_name , teacher.f_name , teacher.t_name) 
        ret['teacher_id'] = teacher.id
        ret['seasons'] = seasons
        ret['inds'] = inds
        ret['res'] = res
       
        return jsonify(ret)
        
@rate_module.route('/addrate' , methods=['GET','POST'])
def addrate():
    if request.method=='POST':
        data=request.values
        print(data)
        d = {'add':True}
        dm.AddRate(int(data['season']),int(data['ind']) ,int(data['teacher']) ,int(data['val']))
        return jsonify(d)