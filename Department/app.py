from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.depart


@app.route("/")
def home():
    if 'username' not in session.keys():
        return redirect('/auth/login')
    return render_template(
        'home.html', **locals())


@app.route("/profile/<string:name>")
def profile(name):
    user = db.users.find_one({"username": name})
    if user is None:
        return error()
    user['id'] = str(user['_id'])
    user.pop('_id')
    return render_template(
        'profile.html', **locals())


@app.route("/delete/<string:name>/")
def delete(name):
    if 'username' not in session.keys():
        return redirect('/auth/login')
    if session['username'] !=name:
        return "Access Denied"
    else:
        db.users.remove({'username': session['username']})
        return logout()


@app.route("/<string:str>/")
def page(str=None):
    if 'username' not in session.keys():
        return redirect('/auth/login')
    return render_template(
        'page.html', **locals())


@app.route("/courses/")
def courses():
    if 'username' not in session.keys():
        return redirect('/auth/login')
    return render_template(
        'courses.html', **locals())


@app.route("/Routine/")
def routine():
    if 'username' not in session.keys():
        return redirect('/auth/login')
    return render_template(
        'routine.html', **locals())


@app.route("/Result/")
def result():
    if 'username' not in session.keys():
        return redirect('/auth/login')
    return render_template(
        'result.html', **locals())


@app.route("/404/")
def error():
    str = '404'
    return render_template(
        'page.html', **locals())


@app.route("/change/")
def change(data=None):
    if 'username' not in session.keys():
        return redirect('/auth/login')
    user = db.users.find_one({"username": session['username']})
    return render_template(
        'change.html', **locals())


@app.route("/auth/login/")
def login(data=None):
    if 'username' in session.keys():
        return redirect('/')
    return render_template(
        'login.html', **locals())


@app.route("/auth/logout")
def logout():
    if 'username' in session.keys():
        session.pop('username')
    return redirect('/')


@app.route("/auth/login-validation", methods=['POST', 'GET'])
def login_validation():
    if request.method == 'POST':
        data = request.form.to_dict()
        username = data['username']
        password = data['password']
        flag = True
        find = db.users.find_one({"username": str(username)})
        if find is None:
            flag = False
            data['username_msg'] = 'Username does not Exist'
        elif find['password'] != password:
            flag = False
            data['password_msg'] = 'Wrong password'
        if flag is False:
            return login(data)
        session['username'] = username
        return redirect('/')


@app.route("/auth/change-validation", methods=['POST', 'GET'])
def change_validation():
    if request.method == 'POST':
        data = request.form.to_dict()
        password_again = data['password_again']
        password = data['password']
        flag=True
        if len(password)<6:
            flag = False
            data['password_msg'] = 'Password should be at least 6 characters'
        if password!=password_again:
            data['password_again_msg'] = 'Password did not match'
            flag=False
        if flag is False:
            return change(data)
        user = db.users.find_one({"username": session['username']})
        db.users.remove({'username': session['username']})
        user['password']=password
        user['marital_status']=data['marital_status']
        user['phn']=data['phn']
        user['addr']=data['addr']
        user['addr1']=data['addr1']
        db.users.insert_one(user)
        return redirect('/')


@app.route("/auth/register")
def register(data=None):
    if 'username' in session.keys():
        return redirect('/')
    return render_template(
        'register.html', **locals())


@app.route("/res", methods=['POST', 'GET'])
def result_entry():
    data = dict()
    data['username']='Bulbul'
    data['course'] = 'Database Management (87859)'
    data['credit'] = 3.00
    data['semester'] = 'Fall'
    data['Session'] = '2015-16'
    data['instructor']= 'John Korth (5785)'
    data['Grade']= 'A+'
    db.results.insert_one(data)
    return "ttt"


@app.route("/auth/register-validation", methods=['POST', 'GET'])
def register_validation():
    if request.method == 'POST':
        data = request.form.to_dict()
        username = data['username']
        password = data['password']
        password_again = data['password_again']
        flag = True
        find = db.users.find_one({"username": str(username)})
        if find is not None:
            flag = False
            data['username_msg'] = 'Username Exists'
        if len(username)<5:
            flag = False
            data['username_msg'] = 'Username should be at least 5 characters'
        if len(password) < 6:
            flag = False
            data['password_msg'] = 'Password should be at least 6 characters'
        if password != password_again:
            data['password_again_msg'] = 'Password did not match'
            flag = False
        if flag is False:
            return register(data)
        #data = dict()
        data['username'] = username
        data['password'] = password
        db.users.insert_one(data)
        return redirect('/')


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(host='127.0.0.2', port=5000, debug=False)