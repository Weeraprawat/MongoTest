import pymongo
from bson import json_util
from flask import Flask,jsonify,render_template,request
#from flask_pymongo import PyMongo

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://admin:BYTitv62935@10.100.2.123:27017")
#client = pymongo.MongoClient("mongodb://admin:BYTitv62935@node9146-advweb-08.app.ruk-com.cloud:11155")

db = client["Member"]

################# Index ###############
@app.route("/")
def index():
    texts = "Hello World , Welcome to MongoDB , By Weeraprawat"
    return texts

############### GET ALL #################
@app.route("/Employees", methods=['GET'])
def get_allEmployees():
    char = db.Employees
    output = char.find()
    return json_util.dumps(output)


@app.route("/test", methods=['GET'])
def get_Join():
    em = db.Employees
    E = em.aggregate( [     
            {
                "$lookup":  {
                        "from" : "Branch",
                        "localField": "Code",
                        "foreignField":"Code" ,
                        "as": "Branch"
                }
            },
            {"$unwind": "$Branch"},
            {
                "$project":{
                    "Name":1,
                    "Title":1,
                    "Location": "$Branch.Location","Province": "$Branch.Province"
                }
            }
        ]  
    )  
    return json_util.dumps(E)

# ###################### GET ONE ############################
@app.route("/Employees/<name>", methods=['GET'])
def get_oneEmployees(name):
    char = db.Employees
    x = char.find_one({'Name' : name})
    if x:
        output = {'Name' : x['Name'],'Title' : x['Title'],
                        'Team' : x['Team'],
                        'Salary' : x['Salary']}
    else:
        output = "No such name"
    return jsonify(output)

# ######################### INSERT ####################
@app.route('/Employees', methods=['POST'])
def add_Employees():
  char = db.Employees
  name = request.json['Name']
  title = request.json['Title']
  team = request.json['Team']
  salary = request.json['Salary']
  
  char_id = char.insert({'Name': name, 'Title': title,
                        'Team': team,
                        'Salary': salary,})
  new_char = char.find_one({'_id': char_id })
  output = {'Name' : new_char['Name'], 'Title' : new_char['Title'],
                        'Team' : new_char['Team'],
                        'Salary' : new_char['Salary'],}
  return jsonify(output)

# ##################### UPDATE ########################
@app.route('/Employees/<name>', methods=['PUT'])
def update_Employees(name):
    char = db.Employees
    x = char.find_one({'Name' : name})
    if x:
        myquery = {'Name' : x['Name'],'Title' : x['Title'],
                        'Team' : x['Team'],
                        'Salary' : x['Salary']}

    name = request.json['Name']
    title = request.json['Title']
    team = request.json['Team']
    salary = request.json['Salary']
    
    newvalues = {"$set" : {'Name' : name, 'Title' : title,
                        'Team' : team,
                        'Salary' : salary}}

    char_id = char.update_one(myquery, newvalues)

    output = {'Name' : name, 'Title' : title,
                        'Team' : team,
                        'Salary' : salary}
    return jsonify(output)

# ##################### DELETE ############################ 
@app.route('/Employees/<name>', methods=['DELETE'])
def delete_Employees(name):
    char = db.Employees
    x = char.find_one({'Name' : name})

    char_id = char.delete_one(x)
    output = "Deleted complete"
    return jsonify(output)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 80)