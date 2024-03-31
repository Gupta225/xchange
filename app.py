from flask import Flask,render_template,request,redirect, session
from flask_pymongo import PyMongo
import  base64

app=Flask(__name__)

app.secret_key = 'rakeshguptakatakam'
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/sign-up')
def signuppage():
    return render_template('signup.html')

@app.route('/log-in')
def loginpage():
    return render_template('login.html')

@app.route('/logging-in',methods=['POST'])
def logging():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user = mongo.db.users.find_one({'username': username})
        if not user:
            return 'User doesnot exists!'
        else:
             if user['password'] == password:
                # session['user_id'] = user['_id']
                session['username'] = username
                profile_img = base64.b64encode(user['profile-img']).decode('utf-8')
                return render_template('/profile.html',user=user,profile_img=profile_img)
             else:
                 return 'password incorrect'
             

@app.route('/signup', methods= ['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        image = request.files['profile-img']
        imagedata=image.read()
        existing_user = mongo.db.users.find_one({'username': username})
        if existing_user:
            return 'Username already exists!'

        new_user = {'username': username, 'password': password,'profile-img':imagedata}
        mongo.db.users.insert_one(new_user)
        
        
        # return 'User created successfully!'
    
    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)