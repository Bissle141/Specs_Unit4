from flask import Flask, render_template, url_for, redirect, flash, session
from forms import TeamForm, ProjectForm, LoginForm, RegisterForm
import os
from model import db, Users, Teams, Projects, connect_to_db

app = Flask(__name__)

app.secret_key = os.environ["SECRET_KEY"]

user_id = 1

@app.route("/")
def home():

    return render_template("home.html")

@app.route("/login-register", methods=["GET", "POST"])
def login_register():
    login_form = LoginForm()
    register_form = RegisterForm()
    
    if login_form.validate_on_submit():
        # check if username is in database
        # if it is check that the password is the same as the one linked to the user
        # if both are true, set session username and user_id then nav to Home page with flash msg
        username = login_form.login_username.data
        password = login_form.login_password.data
        
        user = Users.query.filter_by(username = username).first()
        
        if user is not None:
            if password == user.password:
                session["username"] = username
                session["user_id"] = user.id
                flash("Login Sucessful")
                return redirect(url_for("home"))
            else:
                flash("Wrong password, please try again.")
                return redirect(url_for("login_register"))
        else:
            flash("User does not exits, please try again or a new register.")
            return redirect(url_for("login_register"))
     
    if register_form.validate_on_submit():
        
        new_username = register_form.register_username.data
        new_password = register_form.register_password.data
        
        if Users.query.filter_by(username = new_username).first() is not None:
            flash("Username already in use")
            return redirect(url_for('login_register'))
        
        else:
            new_user = Users(new_username, new_password)
            
            db.session.add(new_user)
            db.session.commit()
            
            flash("Registration complete, please log in.")
            return redirect(url_for("login_register"))
    else:
        for error in register_form.register_password_confirm.errors:
            flash(f"{error}")
        
    return render_template('login_register.html', login_form = login_form, register_form= register_form)

# @app.route("/board/<username>")
@app.route("/board")
def board():
    try: session["username"]
    except:
        flash("Must be logged in to access Board")
        return redirect(url_for('login_register'))
    
    data = {}
    
    teams = Teams.query.filter_by(user_id = session['user_id']).all()
    for team in teams:
        data[team.id] = [team, Projects.query.filter_by(team_id = team.id).all()]
     
    return render_template('board.html', data = data.values())

@app.route("/add-new" )
def add_new():
    team_form = TeamForm()
    
    project_form = ProjectForm()
    project_form.update_teams(Users.query.get(user_id).teams)
    
    return render_template("add_new.html", team_form = team_form, project_form = project_form)

@app.route("/add-team", methods=["POST"])
def add_team():
    team_form = TeamForm()

    if team_form.validate_on_submit():
        team_name = team_form.team_name.data
        new_team = Teams(team_name,user_id)
        
        db.session.add(new_team)
        db.session.commit()
        
        flash('Team added')
        return redirect(url_for("board"))
    else:
        flash('Something went wrong')
        return redirect(url_for("add_new"))
    
@app.route("/add-project", methods=["POST"])
def add_project():
    project_form = ProjectForm()
    project_form.update_teams(Users.query.get(user_id).teams)

    if project_form.validate_on_submit():
        project_name = project_form.project_name.data
        desc = project_form.desc.data
        completed = project_form.completed.data
        team_id = project_form.team_selection.data
        
        new_project = Projects(project_name, desc, completed, team_id)
        db.session.add(new_project)
        db.session.commit()

        flash('Project added')
        return redirect(url_for("board"))
    else:
        flash('Something went wrong')
        return redirect(url_for("add_new"))
    
@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    
    return redirect(url_for("home"))

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug = True)