from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, InputRequired

class TeamForm(FlaskForm):
    team_name = StringField("team name", validators = [DataRequired(), Length(min=4, max=255)])
    submit = SubmitField("submit")
    
class ProjectForm(FlaskForm):
    project_name = StringField("project name", validators= [DataRequired(),Length(min=4, max=255)])
    desc = TextAreaField('desc')
    completed = BooleanField('completed status')
    team_selection = SelectField('team')
    submit = SubmitField("submit")
    
    def update_teams(self, teams):
        self.team_selection.choices = [ (team.id, team.team_name) for team in teams ]
        
class LoginForm(FlaskForm):
    login_username = StringField("username", validators=[InputRequired(), Length(max=255, min=4)])
    login_password = PasswordField("password", validators=[InputRequired()])
    submit = SubmitField("submit")
    
class RegisterForm(FlaskForm):
    register_username = StringField("username", validators=[InputRequired(), Length(max=255, min=4)])
    register_password = PasswordField("password", validators=[InputRequired()])
    submit = SubmitField("submit")
    
    