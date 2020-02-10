from models import User, ToDo, db, database
from flask import Flask, redirect, render_template, request, session, Blueprint, url_for
import sys, random
from flask import current_app as app
from passlib.hash import sha256_crypt
from string import ascii_uppercase, digits, ascii_lowercase


home_ = Blueprint("home", __name__, template_folder='templates', static_folder='static')


@home_.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return redirect(url_for("profile.profile"))


profile_ = Blueprint("profile", __name__, template_folder='templates', static_folder='static')


@profile_.route('/profile')
def profile():
    if session['logged_in']:
        user = User.query.filter_by(name=session['user_name']).first()
        if user.saw == 1:
            things = ToDo.query.filter_by(owner_id=user.id).all()
            return render_template('profile.html', name=session['user_name'], things=things)
        else:
            user.saw = 1
            try:
                database.session.commit()
            except Exception:
                return render_template("database_error.html")
            return render_template("backup_code.html", code=user.backup)
    else:
        return redirect(url_for("home.home"))


add_thing_ = Blueprint("add_thing", __name__, template_folder='templates', static_folder='static')


@add_thing_.route('/profile/add_thing', methods=['POST'])
def add_thing():
    if session['logged_in']:
        user = User.query.filter_by(name=session['user_name']).first()
        things = ToDo.query.filter_by(owner_id=user.id).all()
        if len(request.form['title']) > 0 and len(request.form['content']) > 0:
            new_thing = ToDo(owner_id=user.id, title=request.form['title'], content=request.form['content'])
            try:
                database.session.add(new_thing)
                database.session.commit()

                mycursor = db.mydb_u.cursor()
                mycursor.execute(f"INSERT INTO `{user.name}` (todo_id, owner, title, content) VALUES (NULL, '{user.name}', '{new_thing.title}', '{new_thing.content}')")
                db.mydb_u.commit()
                mycursor.close()

                return redirect(url_for("home.home"))
            except Exception:
                return render_template("database_error.html")
        else:
            error = "Cannot be empty"
            return render_template("profile.html", error=error, name=session['user_name'], things=things)
    else:
        return redirect(url_for("home.home"))


delete_thing_ = Blueprint("delete_thing", __name__, template_folder='templates', static_folder='static')


@delete_thing_.route('/profile/delete_thing', methods=['POST'])
def delete_thing():
    if session['logged_in']:
        user = User.query.filter_by(name=session['user_name']).first()
        try:
            print(request.form['delete'], sys.stdout)
            mycursor = db.mydb_u.cursor()
            mycursor.execute(f"DELETE FROM {user.name} WHERE title = '{request.form['delete']}'")
            mycursor.execute(f"DELETE FROM things WHERE owner_id = '{user.id}' AND title = '{request.form['delete']}'")
            db.mydb_u.commit()
            mycursor.close()

            return redirect(url_for("home.home"))
        except Exception:
            return render_template("database_error.html")
    else:
        return redirect(url_for("home.home"))


login_ = Blueprint("login", __name__, template_folder='templates', static_folder='static')


@login_.route('/login', methods=['POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('home.home'))
    else:
        if len(request.form['p']) > 0 and len(request.form['n']) > 0:
            user = User.query.filter_by(name=request.form['n']).first()
            if user:
                try:
                    if sha256_crypt.verify(str(request.form['p']), str(user.password)) and request.form['n'] == user.name:
                        session['logged_in'] = True
                        session['user_name'] = user.name
                        return redirect(url_for("profile.profile"))
                    else:
                        error = "Wront Creditials"
                        return render_template("index.html", error=error)
                except Exception:
                    error = "Wront Creditials"
                    return render_template("index.html", error=error)
            else:
                error = "Wrong Creditials"
                return render_template("index.html", error=error)
        else:
            error = "Cannot be empty"
            return render_template("index.html", error=error)


register_ = Blueprint("register", __name__, template_folder='templates', static_folder='static')


@register_.route('/register')
def register():
    if session.get('logged_in'):
        return redirect(url_for("home.home"))
    else:
        return render_template('register.html')


register_reg_ = Blueprint("register_reg", __name__, template_folder='templates', static_folder='static')


@register_reg_.route('/register/reg', methods=['Post'])
def register_reg():
    if not session.get('logged_in'):
        if 20 > len(request.form['p']) > 8 and 15 > len(request.form['n']) > 5:
            if User.query.filter_by(name=request.form['n']).first():
                error = "Name Taken"
                return render_template("register.html", error=error)
            else:
                backup = ""
                for i in range(0, 20):
                    backup = backup + random.choice(ascii_uppercase + digits + ascii_lowercase)

                new = User(name=request.form['n'], password=sha256_crypt.encrypt(request.form['p']), backup=backup, saw=0)

                try:
                    #For future app usage
                    mycursor = db.mydb.cursor()
                    mycursor.execute(f"CREATE USER '{new.name}'@'{db.db_address}' IDENTIFIED BY '{new.password}'")
                    mycursor.execute(f"CREATE TABLE `{db.db_database}`.`{new.name}` ( `todo_id` INT NOT NULL AUTO_INCREMENT , `owner` VARCHAR(100) NOT NULL , `title` VARCHAR(100) NOT NULL , `content` VARCHAR(255) NOT NULL , PRIMARY KEY (`todo_id`))")
                    mycursor.close()
                    #
                    mycursor = db.mydb_u.cursor()
                    mycursor.execute(f"GRANT SELECT, INSERT, UPDATE, DELETE ON {new.name} TO '{new.name}'@'{db.db_address}'")
                    db.mydb_u.commit()
                    mycursor.close()
                    #

                    database.session.add(new)
                    database.session.commit()
                except Exception:
                    return render_template("database_error.html")

                info = "User has been created"

                return render_template("register.html", info=info)
        else:
            error = "Cannot be empty or too short / too long"
            return render_template("register.html", error=error)
    else:
        return redirect(url_for("home.home"))


logout_ = Blueprint("logout", __name__, template_folder='templates', static_folder='static')


@logout_.route("/logout", methods=['POST'])
def logout():

    if session['logged_in']:
        session.clear()
        return redirect(url_for("home.home"))
    else:
        return redirect(url_for("home.home"))


forget_ = Blueprint("forget", __name__, template_folder='templates', static_folder='static')


@forget_.route("/forget")
def forget():
    if session.get('logged_in'):
        return redirect(url_for("home.home"))
    else:
        return render_template("forget.html")


forget_get_ = Blueprint("forget_get", __name__, template_folder='templates', static_folder='static')


@forget_get_.route("/forget/forget_get", methods=['POST'])
def forget_get():
    if session.get('logged_in'):
        return redirect(url_for("home.home"))
    else:
        if len(request.form['c']) > 0 and len(request.form['n']) > 0:
            user = User.query.filter_by(name=request.form['n']).first()
            if user:
                if user.name == request.form['n'] and user.backup == request.form['c']:
                    password = ""
                    code = ""

                    for i in range(0, 15):
                        password = password + random.choice(ascii_uppercase + digits + ascii_lowercase)

                    for i in range(0, 20):
                        code = code + random.choice(ascii_uppercase + digits + ascii_lowercase)

                    user.password = sha256_crypt.encrypt(password)
                    user.backup = code
                    try:
                        database.session.commit()
                        #mycursor = db.mydb.cursor()
                        #?#mycursor.execute(f"GRANT CONNECT TO {user.name} IDENTIFIED BY {user.password}")
                        mycursor = db.mydb.cursor()
                        mycursor.execute(f"SET PASSWORD FOR '{user.name}'@'{db.db_address}' = PASSWORD( '{user.password}' )")
                        db.mydb_u.commit()
                    except Exception:
                        return render_template("database_error.html")
                    return render_template("new_pass.html", password=password, code=code)
                else:
                    return render_template("forget.html")
            else:
                error = "User doesn't exist"
                return render_template("forget.html", error=error)
        else:
            error = "Cannot be empty"
            return render_template("forget.html", error=error)


settings_ = Blueprint("settings", __name__, template_folder='templates', static_folder='static')


@settings_.route("/settings", methods=['POST'])
def settings():
    if session['logged_in']:
        return render_template("settings.html", nick=session['user_name'])
    else:
        return redirect(url_for("home.home"))


change_password_ = Blueprint("change_password", __name__, template_folder='templates', static_folder='static')


@change_password_.route("/settings/change_password", methods=['POST'])
def change_password():
    if session['logged_in']:
        user = User.query.filter_by(name=session['user_name']).first()
        if user:
            if len(request.form['c']) > 0 and 20 > len(request.form['p']) > 8 and 20 > len(request.form['p2']) > 8:
                if request.form['c'] == user.backup and request.form['p'] == request.form['p2']:
                    user.password = sha256_crypt.encrypt(request.form['p'])
                    try:
                        database.session.commit()
                        mycursor = db.mydb.cursor()
                        mycursor.execute(f"SET PASSWORD FOR '{user.name}'@'{db.db_address}' = PASSWORD( '{user.password}' )")
                        db.mydb_u.commit()
                        mycursor.close()
                    except Exception:
                        return render_template("database_error.html")

                    info = "Password changed"
                    return render_template("settings.html", info=info)
                else:
                    error = "Wrong Creditials"
                    return render_template("settings.html", error=error, nick=session['user_name'])
            else:
                error = "Cannot be empty or too short / too long"
                return render_template("settings.html", error=error, nick=session['user_name'])
        else:
            return redirect(url_for("home.home"))
    else:
        return redirect(url_for("home.home"))


@app.errorhandler(404)
def not_found(error):
    return render_template("not_found.html")


@app.errorhandler(405)
def not_allowed(error):
    return render_template("not_allowed.html")


@app.errorhandler(500)
def overloaded(error):
    return render_template("overloaded.html")
