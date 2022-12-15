from flask import Flask,Response,request,render_template,redirect,flash
import pymongo
import json
from bson.objectid import ObjectId
app=Flask(__name__)
try:
    mongo=pymongo.MongoClient("mongodb://localhost:27017/")
    db=mongo.UserInfo#userInfo is the name of database will be created if not found
    mongo.server_info()#triger exception if can not connect to db
except:
    print("ERROR CAN NOT CONNECT TO DB")


#home page
@app.route("/")
def home():
    return render_template("home.html")


#CREATE USER
@app.route("/create",methods=['POST'])
def create_user():
    try:
        user_data={"fname":request.form['fname'],
        "lastName":request.form['lname'],
        "age":request.form['age'],
        "email":request.form['email']}
        dbResponse=db.users.insert_one(user_data)#create collection called users and insert data to it
        print("*********",dbResponse)#if we check on local mongo db , will find new db with collection
        return redirect("/read/data")
    except Exception as e:
        print(e)


# #READ all
@app.route('/read/data',methods=['GET'])
def get_some_user():
    try:
        data=list(db.users.find())#we converted it to list to separate each record
        print("####################",data)
        return render_template("all-users.html",data=data)
        
    except Exception as e:
        print(e)
        return Response(
            response=json.dumps({"message":"can not create user"}),
            status=500,
            mimetype="application/json"
        )

# #READ ONE
@app.route('/read/one/<id>',methods=['GET'])#read each record by its id
def get_user_by_id(id):
    try:
        data=db.users.find_one({"_id":ObjectId(id)})
        print("******one user data******",data)
        return render_template("update-user.html",data=data)
        
    except Exception as e:
        print(e)
        return Response(
            response=json.dumps({"message":"can not create user"}),
            status=500,
            mimetype="application/json"
        )
#UPDATE
@app.route('/update/<id>',methods=['POST'])
def update_user(id):
    try:
        response=db.users.update_one(
            {"_id":ObjectId(id)},
            {"$set":{'fname':request.form['fname'],
            'lastName':request.form['lname'],
            'age':request.form['age'],
            'email':request.form['email']}
            })
        print("%%%%%%%%%%%%%%%%%%%%response****************")
        return redirect('/read/data')
    except Exception as e:
        print("&&&&&&&&&&&&&&&&&&&&")
        print(e)
        print("&&&&&&&&&&&&&&&&&&&&")
        return Response(
            response=json.dumps({"message":"sorry user can not update"}),
            status=500,
            mimetype="application/json"
        )




# #DELETE
@app.route('/delete/<id>')
def delete_user(id):
    try:
        dbResponse=db.users.delete_one({"_id":ObjectId(id)})
        return redirect('/read/data')
    except Exception as e:
        print("&&&&&&&&&&&&&&&&&&&&")
        print(e)
        print("&&&&&&&&&&&&&&&&&&&&")
        return Response(
            response=json.dumps({"message":"sorry user can not be deleted"}),
            status=500,
            mimetype="application/json"
        )

if __name__=="__main__":
    app.run(debug=True)
