from flask import request, render_template, redirect, session, flash, url_for, jsonify
from flask import current_app as app
from application.models import User, Tracker, Log
from application.database import db
from application import tasks
from hashlib import md5
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sqlalchemy import desc
from datetime import datetime, timedelta
from pytz import timezone
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt, \
    set_access_cookies

ttypes = ('Multiple Choice', 'Numeric', 'Boolean')

jwt = JWTManager(app)


# @app.after_request
# def refresh_expiring_jwts(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             set_access_cookies(response, access_token)
#         return response
#     except (RuntimeError, KeyError):
#         # Case where there is not a valid JWT. Just return the original response
#         return response

@app.route("/")
def serve_vue_app():
    return render_template("vue/index.html")

@app.route("/hello")
def say_hello():
    job = tasks.hello.apply_async(args = ["World!"],countdown=10)
    #result = job.wait()
    return "Done", 200

@app.route("/app")
def index():
    if "username" in session:
        user = User.query.get(session['user_id'])

        if not user:
            return redirect(url_for('logout'))

        tdata = []
        for tracker in user.trackers.all():
            logs = tracker.logs.all()
            last_log = None
            if logs:
                last_log = tracker.logs.order_by(desc(Log.log_time)).first().log_time
            tdata.append([tracker, last_log])

        return render_template("index.html", tdata=tdata)
    else:
        return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect("/")

    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        uname = request.form.get("uname")
        password = request.form.get("passwd")

        if uname and fname and password:

            p = md5(password.encode())
            passwd = p.hexdigest()

            u = User(first_name=fname, last_name=lname, email=email,
                     username=uname, password=passwd)
            db.session.add(u)
            db.session.commit()
            return redirect("/")
        else:
            flash("Enter correct data!!!")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect("/")

    if request.method == "POST":

        username = request.form.get('username')
        password = request.form.get('passwd')

        if username and password:

            u = User.query.filter(User.username == username).first()

            p = md5(password.encode())

            passwd = p.hexdigest()

            if u and (u.password == passwd):
                session["username"] = username
                session["user_id"] = u.uid
                session["fname"] = u.first_name
                return redirect("/")
            else:
                flash("Invalid Credentials!")

    return render_template("login.html")


@app.route("/api/login", methods=["POST"])
def api_login():
    if request.is_json:

        username = request.json['username']
        password = request.json['password']

        if username and password:

            u = User.query.filter(User.username == username).first()

            p = md5(password.encode())

            passwd = p.hexdigest()

            if u and (u.password == passwd):
                access_token = create_access_token(identity=u.uid)
                return jsonify(message="Login Successful", access_token=access_token,
                               first_name=u.first_name, uid=u.uid)
            else:
                return jsonify(message="Invalid credentials.")
        else:
            return jsonify(message="Invalid credentials.")
    else:
        return jsonify(message="No json found!!")


@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
        session.pop("user_id", "username")
        session.pop("fname", "username")

    return redirect("/")




def get_tracker_plot(tracker_id):
    t = Tracker.query.get(tracker_id)
    logs = t.logs.order_by(Log.log_time).all()
    x = []
    y = []
    if t.tracker_type == 'Multiple Choice':
        temp = []
        for l in logs:
            temp.append(l.value)
        x = list(set(temp))

        for i in x:
            y.append(temp.count(i))

        plt.bar(x, y)
        plt.xlabel('value')
        plt.ylabel('count')
        plt.title(t.name)
        plt.savefig('static/img/plot.png')
        plt.clf()

    elif t.tracker_type == 'Numeric':
        for l in logs:
            x.append(l.log_time)
            try:
                y.append(float(l.value))
            except:
                print("Tracker has few invalid logs")
                x.remove(l.log_time)
                continue

        plt.plot(x, y, linestyle='dotted')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title(t.name)
        plt.savefig('static/img/plot.png')
        plt.clf()

    elif t.tracker_type == 'Boolean':
        temp = []
        for l in logs:
            temp.append(l.value)

        x = ['Yes', 'No']
        y = [temp.count(x[0]), temp.count(x[1])]

        plt.bar(x, y)
        plt.xlabel('value')
        plt.ylabel('count')
        plt.title(t.name)
        plt.savefig('static/img/plot.png')
        plt.clf()

    else:
        print("Wrong tracker type!")


@app.route("/tracker/<int:tid>")
def tracker_details(tid):
    if "username" in session:
        tracker = Tracker.query.get(tid)
        logs = Log.query.filter(Log.tid == tracker.tid)
        if (tracker.tracker_type in ttypes):
            if logs:
                get_tracker_plot(tracker.tid)
            return render_template("tracker_details.html", tracker=tracker, logs=logs)
        else:
            flash("tracker not found!")
            return redirect("/")
    else:
        return redirect("/login")


@app.route("/tracker/create", methods=["GET", 'POST'])
def tracker_create():
    if "username" in session:
        if request.method == 'POST':
            tname = request.form.get("tname")
            desc = request.form.get("desc")
            ttype = request.form.get("ttype")
            settings = request.form.get("settings")

            if tname and (ttype in ttypes):
                t = Tracker(uid=session['user_id'], tracker_type=ttype,
                            name=tname, description=desc, settings=settings)
                db.session.add(t)
                db.session.commit()
                return redirect("/")
        return render_template("add_tracker.html")
    else:
        return redirect("/login")


@app.route("/tracker/<int:tid>/delete")
def tracker_delete(tid):
    if "username" in session:

        tracker = Tracker.query.get(tid)
        if tracker:
            Log.query.filter(Log.tid == tracker.tid).delete()
            db.session.delete(tracker)
            db.session.commit()
        else:
            flash("Something went wrong!")
        return redirect("/")
    else:
        return redirect("/login")


@app.route("/tracker/<int:tid>/edit", methods=['GET', 'POST'])
def tracker_edit(tid):
    if "username" in session:
        tracker = Tracker.query.get(tid)
        if tracker:
            if request.method == 'POST':
                desc = request.form['desc']
                ttype = request.form['ttype']
                settings = request.form['settings']

                if ttype in ttypes:
                    tracker.description = desc
                    tracker.tracker_type = ttype
                    tracker.settings = settings

                    db.session.add(tracker)
                    db.session.commit()
                    return redirect("/")

            return render_template("edit_tracker.html", tracker=tracker)
        else:
            flash("Something went wrong!")
            return redirect("/")
    else:
        return redirect("/login")


@app.route("/tracker/<int:t_id>/log/create/", methods=['GET', 'POST'])
def create_tracker_log(t_id):
    if "username" in session:
        tracker = Tracker.query.get(t_id)
        if tracker:
            options = None
            if tracker.tracker_type == "Multiple Choice":
                options = [i.strip() for i in tracker.settings.split(",")]
            if request.method == 'POST':
                tval = request.form['tval']
                notes = request.form['tnotes']

                if tracker.tracker_type == "Numeric":
                    try:
                        temp = float(tval)
                        #print("Unknown numeric value", temp)
                    except:
                        flash("Please enter numeric value")
                        return render_template("add_tracker_log.html", tracker=tracker, options=options)
                if tracker.tracker_type == "Multiple Choice":
                    if tval not in options:
                        flash("Please enter appropriate option")
                        return render_template("add_tracker_log.html", tracker=tracker, options=options)
                if tracker.tracker_type == "Boolean":
                    if tval not in ["Yes", "No"]:
                        flash("Please enter appropriate option")
                        return render_template("add_tracker_log.html", tracker=tracker, options=options)

                lg = Log(tid=tracker.tid, value=tval, notes=notes)
                db.session.add(lg)

                db.session.flush()

                tracker.last_tracked = lg.log_time
                db.session.add(tracker)

                db.session.commit()
                return redirect(url_for("tracker_details", tid=tracker.tid))
            return render_template("add_tracker_log.html", tracker=tracker, options=options)
        else:
            flash("tracker not found!")
            return redirect("/")
    else:
        return redirect("/login")


@app.route("/tracker/<int:t_id>/logs")
def get_all_tracker_logs(t_id):
    if "username" in session:
        tracker = Tracker.query.get(t_id)
        logs = Log.query.filter(Log.tid == tracker.tid).all()
        if tracker and logs:
            return render_template("get_all_tracker_logs.html", tracker=tracker, logs=logs)
        else:
            flash("something went wrong!")
            return redirect("/")
    else:
        return redirect("/login")


@app.route("/tracker/<int:t_id>/log/<int:l_id>")
def get_tracker_log(t_id, l_id):
    if "username" in session:
        tracker = Tracker.query.get(t_id)
        log = Log.query.get(l_id)
        if tracker and log:
            return render_template("get_tracker_log.html", tracker=tracker, log=log)
        else:
            flash("something went wrong!")
            return redirect("/")
    else:
        return redirect("/login")


@app.route("/tracker/<int:t_id>/log/<int:l_id>/edit", methods=['GET', 'POST'])
def edit_tracker_log(t_id, l_id):
    if "username" in session:
        tracker = Tracker.query.get(t_id)
        log = Log.query.get(l_id)
        if tracker and log:
            options = None
            if tracker.tracker_type == "Multiple Choice":
                options = [i.strip() for i in tracker.settings.split(",")]

            if request.method == 'POST':
                tval = request.form['tval']
                notes = request.form['tnotes']

                log.value = tval
                log.notes = notes
                db.session.add(log)
                db.session.commit()
                return redirect(url_for("tracker_details", tid=tracker.tid))
            return render_template("edit_tracker_log.html", tracker=tracker, log=log, options=options)
        else:
            flash("something went wrong!")
            return redirect("/")
    else:
        return redirect("/login")


@app.route("/tracker/<int:t_id>/log/<int:l_id>/delete")
def delete_tracker_log(t_id, l_id):
    if "username" in session:
        tracker = Tracker.query.get(t_id)
        log = Log.query.get(l_id)
        if tracker and log:
            db.session.delete(log)
            db.session.commit()
            return redirect(url_for('tracker_details', tid=tracker.tid))
        else:
            flash("something went wrong!")
            return redirect("/")
    else:
        return redirect("/login")
