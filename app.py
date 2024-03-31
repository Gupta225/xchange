from flask import Flask,render_template,request,redirect, url_for,session,flash,jsonify
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
        item = mongo.db.items.find({'username': username}, {'item_image': 1})
        encoded_images = []
        for item_image in item:
            encoded_image = base64.b64encode(item_image['item_image']).decode('utf-8')
            encoded_images.append(encoded_image)
        if not user:
            return render_template('login.html',message="user does not exist")
        else:
             if user['password'] == password:
                # session['user_id'] = user['_id']
                session['username'] = username
                profile_img = base64.b64encode(user['profile-img']).decode('utf-8')
                return render_template('/profile.html',user=user,profile_img=profile_img,message='logged in successfully',encoded_images=encoded_images)
             else:
                 return render_template('login.html',message="invalid username or password")
             

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
        # existing = mongo.db.items.find_one({'username': username})


        
        
        # return 'User created successfully!'
    
    return render_template('login.html')


@app.route('/add')
def add():
    return render_template('additem.html')
@app.route('/logout')
def logout():
    session.pop('username', None)  
    return redirect(url_for('loginpage'))
@app.route('/check')
def check():
    if 'username' in session:
        username = session['username']
        return f"The username '{username}' is stored in the session."
    else:
        return "No username stored in the session."
@app.route('/addingitem', methods= ['POST'])
def  addingitem():
    if request.method=='POST':
        itemname=request.form['item_name']
        itemcost=request.form['item_cost']
        itemimg=request.files['item_image']
        imgdata=itemimg.read()
        username = session.get('username')

        if username:
            new_item = {
                'username': username,
                'item_name': itemname,
                'item_cost': itemcost,
                'item_image': imgdata  
            }
            
            mongo.db.items.insert_one(new_item)
            
            return 'item added successfully'
        else:
            return 'User not logged in. Please log in to add items.'
        

# @app.route('/get-user-items', methods=['GET'])
# def get_user_items():
#     # Get the username from the session
#     username = session.get('username')
#     if username:
#         # Query MongoDB to get items belonging to the specific user
#         items = mongo.db.items.find({'username': username})

#         # Convert MongoDB cursor to list of dictionaries
#         items_list = list(items)

#         # Return items as JSON
#         return jsonify({'error': 'User not logged in'})
#     else:
#         # If user is not logged in, return an error message
#         return jsonify({'error': 'User not logged in'})
    
if __name__ == '__main__':
    app.run(debug=True)