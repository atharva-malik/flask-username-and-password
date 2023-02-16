from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


try:
    with open("users.json", "r") as f:
        users = json.load(f)
except FileNotFoundError:
    users = {}


def initial_retrieve_password():
    try:
        with open("storedPasses.json", "r") as f:
            # Load the contents of the file into a dictionary
            data = json.load(f)
            return data
    except Exception:
        return {}


passwords = initial_retrieve_password()


def retrieve_password(user):
    password = users[user]["password"]
    return password


def authenticate_user(username, password):
    if username in users and users[username]["password"] == password:
        return True
    else:
        return False


def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)


def add_user(username, password):
    users[username] = {"password": password}
    save_users()


@app.route('/signup', methods=['GET', 'POST'])
def signup_form_submission():
    message = ""
    if request.method == "POST":
        name = request.form['name']
        password = request.form["password"]
        if name in users:
            message = "Username taken!"
            return render_template('signup.html', message=message)
        else:
            add_user(name, password)
            save_users()
            return redirect("/")
    return render_template('signup.html', message=message)


@app.route('/login', methods=['GET', 'POST'])
def form_submission():
    message = ""
    if request.method == "POST":
        name = request.form['name']
        password = request.form["password"]
        if name in users and password in users[name]["password"]:
            return redirect("/login_done")
        else:
            return redirect("/login_failed")
    return render_template('login.html', message=message)


@app.route('/login_done')
def user_authenticated():
    return "Authenticated"


@app.route('/login_failed')
def user_not_authenticated():
    return "Failed"


@app.route('/admin')
def admin():
    users_list = []
    a = 1
    indexOfUsers_list = 0
    for user in users:
        username = ""
        for letter in user:
            if a <= 2:
                username += letter
                a += 1
            else:
                username += "*"
        users_list.append(username)
        a = 1
    for user in users:
        the_password = users[user]['password']
        password = ""
        for letter in the_password:
            if a <= len(the_password) - 2:
                password += "*"
                a += 1
            else:
                password += users[user]['password'][-2:]
                break
        users_list[indexOfUsers_list] += ": " + password
        a = 1
        indexOfUsers_list += 1
    return render_template('admin.html', users=users_list)


if __name__ == '__main__':
    app.run(debug=True)
