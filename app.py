from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://biqhualriwkteu:7b0aafffa35665ba7417f2e9c6a54cd4d5f6a15aa8340c7acbb779f92bebea75@ec2-44-192-245-97.compute-1.amazonaws.com:5432/d363duf4ilahub"
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


        

# class Date(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     day = db.Column(db.Integer, nullable = False)
#     quote = db.Column(db.Integer, nullable = False)

    # def __init__(self,day, quote):
    #     self.day = day
    #     self.quote = quote


class DataSchema(ma.Schema):
    class Meta:
        fields = ( "id", "name", "email", "password")

data_schema = DataSchema()
multiple_data_schema = DataSchema(many = True)

@app.route("/user/add", methods = ["POST"])
def add_user():
    if request.content_type != "application/json":
        return jsonify("ERROR Data must be sent as JSON.")

    post_data = request.get_json()
    # id = post_data.get(id)
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
    # id = post_data.get(id)
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

