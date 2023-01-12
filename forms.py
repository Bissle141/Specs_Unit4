from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

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
    