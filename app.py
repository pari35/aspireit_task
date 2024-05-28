from flask import Flask, render_template, request, url_for, redirect, session
from pymongo import MongoClient
import bcrypt
from werkzeug.utils import secure_filename
import os
from werkzeug.exceptions import RequestEntityTooLarge

#set app as a Flask instance 
app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 *1024
app.config['ALLOWED_EXTENTIONS'] = ['.jpg','.jpeg','.png','.gif']
#encryption relies on secret keys so they could be run
app.secret_key = "testing"
# client = MongoClient("mongodb+srv://paritoshpardeshi35:ksIwimVdcCXlFxD4@cluster0.qoagclq.mongodb.net/")
# db = client.get_database("total records")
def MongoDB():
    client = MongoClient("mongodb+srv://paritoshpardeshi35:ksIwimVdcCXlFxD4@cluster0.qoagclq.mongodb.net/")
    db = client.get_database('total_records')
    records = db.register
    return records
# records = db.register
app.route('/',methods=['post','get'])

 #connect to your Mongo DB database
def dockerMongoDB():
    client = MongoClient("mongodb+srv://paritoshpardeshi35:ksIwimVdcCXlFxD4@cluster0.qoagclq.mongodb.net/")
    db = client.get_database('total_records')
    records = db.register,
    pw = "test123"
    hashed = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
    records = db.register
    records.insert_one({
        "name": "Test Test",
        "email": "test@yahoo.com",
        "password": hashed
    })
    return records

records = dockerMongoDB()


@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    #if method post in index
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #if found in database showcase that it's found 
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            #hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            #assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, 'password': hashed}
            #insert it in the record collection
            records.insert_one(user_input)
            
            #find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            #if registered redirect to logged in as the registered user
            return render_template('logged_in.html', email=new_email)
    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #check if email exists in database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html', email=email)
    else:
        return redirect(url_for("login"))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')

@app.route("/media",methods=["POST","GET"])
def media():
  images = []
#   for file in files:
#       extention = os.path.splitext(file)[1].lower()
#       if extention in app.config['ALLOWED_EXTENTIONS']:
#           images.append(file)
#   files = os.listdir(app.config['ALLOWED_EXTENTIONS'])

  return render_template('upload.html',images =images)

@app.route("/upload",methods =['POST'])
def upload():
    file = request.files['file']
    extention =os.path.splitext(file.filename)
    print(extention)

    if file:
        file.save(os.path.join('uploads/',secure_filename(file.filename)))
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)