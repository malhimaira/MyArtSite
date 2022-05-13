from datetime import datetime
import mysql.connector
import os
from flask import Flask, render_template, session, redirect, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from forms import SignInForm, ContactForm, ForgotPass

app = Flask(__name__)
app.secret_key = 'hello'

maidb = mysql.connector.connect(
  host="localhost",
  user=os.environ["USERmai"],
  password=os.environ["PASSmai"],
  database = 'mydatabase'
)

mycursor = maidb.cursor()


@app.route('/')
def default():
    return render_template('MyHome.html', username=session.get('username'))


@app.route('/HOME')
def homes():
    return render_template('MyHome.html')


@app.route('/PAINT')
def paints():
    return render_template('MyPaint.html')


@app.route('/PENCIL')
def pencils():
    return render_template('MyPencil.html')


@app.route('/INVENTORY')
def inventory():
    return render_template('MyInventory.html')


@app.route('/MIXEDMEDIA')
def mixmed():
    return render_template('MyMixMed.html')


@app.route('/TIPSANDTUTORIALS')
def tipstuts():
    return render_template('MyTipTut.html')


@app.route('/CONTACT', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        sql = "INSERT INTO contactmessages (time, name, emailaddress, message) VALUES (%s, %s, %s, %s)"
        val = (dt_string, form.name.data, form.email.data, form.message.data)
        mycursor.execute(sql, val)
        maidb.commit()

    return render_template('MyContact.html', form=form)

@app.route('/POSTS', methods=['GET', 'POST'])
@login_required
def post():
    cname = []
    cemail = []
    cmess = []
    auser = []
    aname = []

    mycursor.execute("SELECT time, name, emailaddress, message FROM contactmessages")

    fetchedDt = mycursor.fetchall()
    cnt =0
    timestanp =''
    for row in fetchedDt:
        for elem in row:
            if cnt==0:
                timestamp = elem
            if cnt==1:
                cname.append(elem)
            if cnt == 2:
                cemail.append(elem)
            if cnt == 3:
                cmess.append(timestamp+' '+elem)
            cnt +=1

    mycursor.execute("SELECT name FROM admins")
    fetchedDt = mycursor.fetchall()
    for row in fetchedDt:
        for elem in row:
            auser.append(elem)

    return render_template('MyPosts.html', username=session.get('username'), cname=cname, cemail=cemail, cmess=cmess,
                           auser=auser, aname=aname)


def check_pass(username, password):

    mycursor.execute("SELECT name, pass FROM admins")

    myresult = mycursor.fetchall()

    truthChck =0
    for row in myresult:
        print(row)
        cnt = 0
        for elem in row:
            print(elem)
            if cnt == 0 and elem == username:
                print("user ac")
                truthChck +=1
            elif cnt == 1 and elem == password:
                print("passed ac")
                truthChck +=1
            if truthChck ==2:
                return True
            cnt +=1
        truthChck = 0
        cnt = 0
    return False


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/ADMIN'
app.config['USE_SESSION_FOR_NEXT'] = True


class User(UserMixin):
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/ADMIN', methods=['GET', 'POST'])
def admin():
    form = SignInForm()
    if form.validate_on_submit():
        if check_pass(form.username.data, form.password.data):
            login_user(User(form.username.data))
            flash('Logged in successfully.')
            next_page = session.get('next', '/POSTS')
            session['next'] = '/POSTS'
            return redirect(next_page)
        else:
            flash('Invalid Admin username/password')
    return render_template('MyAdmin.html', form=form)


# @app.route('/FORGOT', methods=['GET', 'POST'])
# def forgot():
#     form = ForgotPass()
#     if form.validate_on_submit():
#         if check_pass(form.usersname.data, form.oldpass.data):
#             with open('data/USERS.csv', 'a') as f:
#                 writer = csv.writer(f)
#                 writer.writerow([form.usersname.data, form.newpass.data, form.realname.data])
#                 return redirect(url_for('forgotpage', name=form.realname.data))
#         else:
#             flash('Invalid Admin username/password')
#     return render_template('MyForgot.html', form=form)
#
#
# @app.route('/forgotpage/<name>')
# def forgotpage(name):
#     return render_template('MyForgotSubmit.html', name=name)


@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run()
