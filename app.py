from flask import Flask, request, session, redirect, url_for, render_template
import my_user_model as model
import json
import os

app = Flask(__name__, template_folder="views")
app.secret_key = os.urandom(20)
user = model.User()


@app.route("/users", methods=['GET', 'POST', 'PUT', 'DELETE'])
def users():
    if request.method == 'GET':
        help = user.all()
        result = []
        for l in help:
            result.append([l[0], l[1], l[2], l[3], l[5]])
        return f"<h1>{result}</h1>"
    elif request.method == 'POST':
        data = [request.form.get('firstname', ''), request.form.get('lastname', ''), request.form.get('age', ''),
                request.form.get('password', ''), request.form.get('email', '')]
        user.create_user(data)
        return f"<h1>ok</h1>"
    elif request.method == 'PUT':
        if session['userid']:
            result = user.update(session['userid'], 'password', request.form.get('password'))
            return f"<h1>{result}</h1>"
        return f"<h1>not passed</h1>"
    elif request.method == 'DELETE':
        if session['userid']:
            user.destroy(session['userid'])
            return redirect(url_for("sign_out"))
        return f"<h1>not deleted</h1>"


@app.route("/sign_in", methods=['POST'])
def sign_in():
    if request.method == 'POST':
        user_lists = user.all()
        password = request.form.get('password')
        email = request.form.get('email')
        user_list = list(filter(lambda x: x[4] == password and x[5] == email, user_lists))
        if len(user_list) > 0:
            userid = user_list[0][0]
            session['userid'] = userid
            return f"<h1>signed in</h1>"
        return f"<h1>not signed</h1>"


@app.route("/sign_out", methods=['DELETE'])
def sign_out():
    if request.method == 'DELETE':
        if not session.get("userid") is None:
            session.pop('userid', None)
            return f"<h1>signed out</h1>"
        return f"<h1>not signed out</h1>"


@app.route("/")
def index():
    help = user.all()
    return render_template('index.html', lists=help)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("8080"))
