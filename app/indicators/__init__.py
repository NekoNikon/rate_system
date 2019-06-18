from flask import Blueprint, request, render_template , jsonify
from app.database.smdb import DataManager


dm = DataManager()

ind_module = Blueprint('ind',__name__)

@ind_module.route('/edit_inds' , methods=['GET','POST'])
def edit_inds():
    records = dm.GetIndsWithGroup()
    return jsonify(records)
    
@ind_module.route('/edit_season' , methods=['GET','POST'])
def edit_season():
    records = dm.GetSeasonsId()
    return jsonify(records)

@ind_module.route('/add_group_ind' , methods=['GET','POST'])
def add_group_ind():
    dm.AddGroupInds(request.values['name'])
    d = {'del':True}
    return jsonify(d)

@ind_module.route('/delete_group_ind' , methods=['GET','POST'])
def delete_group_ind():
    dm.DelGroupInds(int(request.values['id']))
    d = {'del':True}
    return jsonify(d)

@ind_module.route('/add_ind' , methods=['GET','POST'])
def add_ind():
    dm.AddInd(int(request.values['id']) , request.values['name'])
    d = {'del':True}
    return jsonify(d)

@ind_module.route('/update_group_ind' , methods=['GET','POST'])
def update_group_ind():
    data = request.values
    dm.UpdateGroupInd(int(data['id']) , data['value'])
    print('update')
    d = {'del':True}
    return jsonify(d)

@ind_module.route('/delete_ind' , methods=['GET' , 'POST'])
def delete_ind():
    dm.DelInd(int(request.values['id']))
    d = {'del':True}
    return jsonify(d)

@ind_module.route('/update_ind' , methods=['GET' , 'POST'])
def update_ind():
    dm.UpdateInd(int(request.values['id']) , request.values['name'])
    d = {'del':True}
    return jsonify(d)