import os
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from models import db,Employee


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:sheetal@localhost/emp"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
# # app.config['SQLALCHEMY_BINDS'] = None
# comment

db.init_app(app)

@app.before_first_request
def create_table():
  db.create_all()


# Home page 
@app.route('/')
def get():
  return "Hello , Happy New Year"

# get details of all employee
@app.route('/emp',methods=['GET'])
def get_emp_all():
  all_rows = Employee.query.all()
  emp = {}
  for i in all_rows:
    emp[i.id] = [i.name,i.id,i.age]
    
  return jsonify({"success": emp })


# get detail by name 
@app.route('/emp/<string:name>',methods=['GET'])
def get_emp(name):
  employees = Employee.query.filter_by(name=name)
  if employees:
    emp = {}
    for i in employees:
      emp[i.id] = [i.name,i.id,i.age]

    return jsonify({"success": emp})

  return jsonify({"error": "Employee not Found !!!" })

# Adding data into database
@app.route('/emp/add',methods=['POST'])
def create_emp():

  req = request.get_json()

  new_emp = Employee(req['id'],req['name'],req['age'])
  db.session.add(new_emp)
  db.session.commit()

  return jsonify({
    "success":"Data added successfully",
  })

# update database
@app.route('/emp/update/<int:id>',methods=['PUT'])
def update_emp_details(id):

  employees = Employee.query.filter_by(id=id).first()
  if employees:
    
    db.session.delete(employees)
    db.session.commit()

    req = request.get_json()
    id = req['id']
    name = req['name']
    age = req['age']

    updated_data = Employee(id,name,age)
    db.session.add(updated_data)
    db.session.commit()

    return jsonify({"success": "Successfully Updated","data":[id,name,age]})

  return jsonify({"error": "Employee not Found !!!" })

# delete emp details
@app.route('/emp/delete/<int:id>',methods=['DELETE'])
def delete_emp(id):
  employee = Employee.query.filter_by(id=id).first()
  if employee:
    db.session.delete(employee)
    db.session.commit()

    return jsonify({"Success":"Employee data deleted"})

  return jsonify({"error":"Employee not found"})
 
app.debug=True
if __name__=="__main__":
    app.run(host='0.0.0.0')