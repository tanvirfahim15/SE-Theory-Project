from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.duerp


@app.route("/")
def home():
    if 'username' not in session.keys():
        return redirect('/auth/login')
    return render_template(
        'home.html', **locals())


@app.route("/profile/<string:name>")
def profile(name):
    if 'username' not in session.keys():
        return redirect('/auth/login')
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


@app.route("/change/")
def change(data=None):
    if 'username' not in session.keys():
        return redirect('/auth/login')
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
        db.users.remove({'username': session['username']})
        data = dict()
        data['username'] = session['username']
        data['password'] = password
        db.users.insert_one(data)
        return redirect('/')


@app.route("/auth/register")
def register(data=None):
    if 'username' in session.keys():
        return redirect('/')
    return render_template(
        'register.html', **locals())


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
        data = dict()
        data['username'] = username
        data['password'] = password
        db.users.insert_one(data)
        return redirect('/')


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(host='127.0.0.1', port=5000, debug=False)