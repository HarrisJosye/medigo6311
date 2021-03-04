from flask import (Flask, redirect, render_template, request, session, url_for)


class client:
    def __init__(self, id_no, username, password):
        self.id = id_no
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User : {self.username}>'


clients = []
clients.append(client(id_no=1, username='admin', password='admin'))
clients.append(client(id_no=2, username='mandeepmandla97@gmail.com', password='mandeep'))

# class registration:
#     def __init__(self, id_no, username, password, email, contact):
#         self.id = id_no
#         self.username = username
#         self.password = password
#         self.email = email
#         self.contact = contact


app = Flask(__name__)
app.secret_key = 'idontknowitsroleyetbutneedit'


@app.route('/')
def welcome_page():
    return render_template('welcome_page.html')


@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        session.pop('client_id', None)
        username = request.form['username']
        password = request.form['password']

        user_details = [x for x in clients if x.username == username][0]
        if user_details and user_details.password == password:
            session['client_id'] = user_details.id
            session['username'] = user_details.username
            return redirect(url_for('welcome_page'))
        else:
            return redirect(url_for('login_page'))

    return render_template('login_page.html')


@app.route('/signup_page', methods=['GET', 'POST'])
def signup_page():
    # error = ''
    # if "username" in session:
    #     return redirect(url_for('login_page'))
    # if request.method == 'POST':
    #     user = request.form.get("username")
    #     email = request.form.get("Email-id")
    #
    #     password_1 = request.form.get("Password")
    #     password_2 = request.form.get("Confirm-Password")
    #
    #     category = request.form.get("Category")
    return render_template('signup_page.html')


if __name__ == '__main__':
    app.run()
