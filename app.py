import csv
from datetime import datetime

from flask import Flask, render_template, session, redirect, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from forms import SignInForm, ContactForm, ForgotPass

app = Flask(__name__)
app.secret_key = 'hello'


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
        with open('data/MESSAGES.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([form.name.data, form.email.data, form.message.data])
            return redirect(url_for('contact_response', name=form.name.data))
    return render_template('MyContact.html', form=form)


@app.route('/contact_response/<name>')
def contact_response(name):
    return render_template('MyContactSubmit.html', name=name)


@app.route('/POSTS', methods=['GET', 'POST'])
@login_required
def post():
    cname = []
    cemail = []
    cmess = []
    auser = []
    aname = []
    with open('data/MESSAGES.csv') as file:
        reader = csv.reader(file)
        for user in reader:
            name = user[0]
            cname.append(name)
            email = user[1]
            cemail.append(email)
            mess = user[2]
            cmess.append(mess)
    with open('data/USERS.csv') as f:
        reader2 = csv.reader(f)
        for user2 in reader2:
            username = user2[0]
            auser.append(username)
            name = user2[2]
            aname.append(name)
    return render_template('MyPosts.html', username=session.get('username'), cname=cname, cemail=cemail, cmess=cmess,
                           auser=auser, aname=aname)


def check_pass(username, password):
    with open('data/USERS.csv') as f:
        for user in csv.reader(f):
            if username == user[0] and password == user[1]:
                return True
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


@app.route('/FORGOT', methods=['GET', 'POST'])
def forgot():
    form = ForgotPass()
    if form.validate_on_submit():
        if check_pass(form.usersname.data, form.oldpass.data):
            with open('data/USERS.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([form.usersname.data, form.newpass.data, form.realname.data])
                return redirect(url_for('forgotpage', name=form.realname.data))
        else:
            flash('Invalid Admin username/password')
    return render_template('MyForgot.html', form=form)


@app.route('/forgotpage/<name>')
def forgotpage(name):
    return render_template('MyForgotSubmit.html', name=name)


@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run()
