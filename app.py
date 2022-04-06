from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://knxhprornpmgmg:300344413e79cd40922f039d50374b8c5bdb1a060c6519861740a9a2ec6c8310@ec2-44-195-191-252.compute-1.amazonaws.com:5432/d7q82an41ckn05"
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique=True)
    password = db.Column(db.String, nullable = False)
    

    def __init__(self, name, email,password):
        self.name = name
        self.email = email
        self.password = password

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable = False)


    def __init__(self, text):
        self.text = text




class DataSchema(ma.Schema):
    class Meta:
        fields = ( "id", "name", "email", "password")

data_schema = DataSchema()
multiple_data_schema = DataSchema(many = True)


class TaskSchema(ma.Schema):
    class Meta:
        fields = ( "id", "text")

task_schema = TaskSchema()
multiple_task_schema = TaskSchema(many = True)


@app.route("/task/add", methods = ["POST"])
def add_task():
    if request.content_type != "application/json;charset=UTF-8": 
        print("this is working", request.content_type)
        return jsonify("ERROR Data must be sent as JSON.")

    post_data = request.get_json()
    text = post_data.get("text")
   

    record = Task(text)
    db.session.add(record)
    db.session.commit()

    return jsonify(task_schema.dump(record))



@app.route("/task/get", methods = ["GET"])
def get_all_tasks():
    
   

    records = db.session.query(Task).all()
    return jsonify(multiple_task_schema.dump(records))


@app.route("/task/get/<id>", methods = ["GET"])
def get_task_by_id(id):
    

    record = db.session.query(Task).filter(Task.id == id).first()
    return jsonify(task_schema.dump(record))


@app.route("/task/update/<id>", methods = ["PUT"])
def update_task(id):
    record = db.session.query(Task).filter(Task.id == id).first()
    if record is None:
        return jsonify(F"No task with id {id}")


    put_data = request.get_json()
    text = put_data.get("text")
    
    


    db.session.commit()
    return jsonify(task_schema.dump(record))




@app.route("/task/delete/<id>", methods = ["DELETE"])
def delete_task(id):
    if request.content_type != "application/json":
        return jsonify("ERROR Data must be sent as JSON.")

    
    record = db.session.query(Task).filter(Task.id == id).first()
    db.session.delete(record)
    db.session.commit()
    return jsonify(task_schema.dump(record))




@app.route("/user/add", methods = ["POST"])
def add_user():
    if request.content_type != "application/json":
        return jsonify("ERROR Data must be sent as JSON.")

    post_data = request.get_json()
    name = post_data.get("name")
    email = post_data.get("email")
    password = post_data.get("password")

   

    record = Data(name, email,password)
    db.session.add(record)
    db.session.commit()

    return jsonify(data_schema.dump(record))



@app.route("/user/get", methods = ["GET"])
def get_all_users():
    if request.content_type != "application/json":
        return jsonify("ERROR Data must be sent as JSON.")

    post_data = request.get_json()
    name = post_data.get("name")
    email = post_data.get("email")
    password = post_data.get("password")

   

    records = db.session.query(Data).all()
    return jsonify(multiple_data_schema.dump(records))


@app.route("/user/get/<id>", methods = ["GET"])
def get_user_by_id(id):
    if request.content_type != "application/json":
        return jsonify("ERROR Data must be sent as JSON.")

    record = db.session.query(Data).filter(Data.id == id).first()
    return jsonify(data_schema.dump(record))


@app.route("/user/update/<id>", methods = ["PUT"])
def update_user(id):
    record = db.session.query(Data).filter(Data.id == id).first()
    if record is None:
        return jsonify(F"No user with id {id}")


    put_data = request.get_json()
    name = put_data.get("name")
    email = put_data.get("email")
    password = put_data.get("password")
    


    db.session.commit()
    return jsonify(data_schema.dump(record))




@app.route("/user/delete/<id>", methods = ["DELETE"])
def delete_user(id):
    if request.content_type != "application/json":
        return jsonify("ERROR Data must be sent as JSON.")

    
    record = db.session.query(Data).filter(Data.id == id).first()
    db.session.delete(record)
    db.session.commit()
    return jsonify(data_schema.dump(record))











if __name__ == "__main__":
    app.run(debug=True)

