from flask import Flask, render_template, url_for, redirect, flash, session
from forms import TeamForm, ProjectForm, LoginForm, RegisterForm
import os
from model import db, Users, Teams, Projects, connect_to_db

app = Flask(__name__)

app.secret_key = os.environ["SECRET_KEY"]

user_id = 1

@app.route("/")
def home():
    team_form = TeamForm()
    
    project_form = ProjectForm()
    project_form.update_teams(Users.query.get(user_id).teams)

    return render_template("home.html", team_form = team_form, project_form = project_form)

@app.route("/login-register")
def login_register():
    login_form = LoginForm()
    register_form = RegisterForm()
    
    if login_form.validate_on_submit:
        # check if username is in database
        # if it is check that the password is the same as the one linked to the user
        # if both are true, set session username and user_id then nav to Home page with flash msg
        username = login_form.login_username
        password = login_form.login_password
        print(username,password)
        
        
    return render_template('login_register.html', login_form = login_form, register_form= register_form)

# @app.route("/board/<username>")
@app.route("/board")
def board():
    return render_template('board.html')

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
    del session.username
    del session.user_id

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug = True)