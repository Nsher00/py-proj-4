from flask import Flask, render_template, redirect, url_for, session
from forms import TeamForm, ProjectForm, LoginForm
from model import db,connect_to_db,User,Team,Project

app = Flask(__name__)
app.secret_key = "secrettunnel"

USER_ID = 1


@app.route("/")
def home():
    team_form = TeamForm()
    project_form = ProjectForm()
    user_form = LoginForm()
    project_form.update_teams(User.query.get(USER_ID).teams)
    return render_template("home.html",team_form=team_form, project_form=project_form, user_form=user_form)

@app.route('/add-team', methods=['POST'])
def add_team():
    team_form = TeamForm()
    if team_form.validate_on_submit():
        team_name = team_form.team_name.data
        new_team = Team(team_name, USER_ID)
        db.session.add(new_team)
        db.session.commit()
    return redirect(url_for("home"))

@app.route('/add-project', methods=['POST'])
def add_project():
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(USER_ID).teams)
    if project_form.validate_on_submit():
        project_name = project_form.project_name.data
        description = project_form.description.data
        completed = project_form.completed.data
        team_selection = project_form.team_selection.data

        new_project = Project(project_name, description, completed, team_selection)

        db.session.add(new_project)
        db.session.commit()
    return redirect(url_for("home"))

@app.route('/add-user', methods=['POST'])
def add_user():
    user_form = LoginForm()
    if user_form.validate_on_submit():
        username = user_form.username.data
        password = user_form.password.data

        new_user = User(username, password)

        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for("home"))

@app.route('/login')
def login():
    login_form = LoginForm()
    return render_template('login.html', login_form=login_form)

@app.route('/login-user', methods=['GET','POST'])
def login_user():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter_by(username=username).first()
        if not user or user.password != password:
            return redirect(url_for('login'))
    
        session['username'] = user.username
        session['id'] = user.id
        print(user.teams)
    return redirect(url_for('user'))

@app.route('/user')
def user():
    user = User.query.filter_by(username=session['username']).first()
    user_id = user.id
    print(user_id)
    return render_template('user.html', user=user)

@app.route('/logout')
def logout():
      '''Logs the user out.'''
      del session['username']
      return redirect(url_for("login"))

        
if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)