from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from .actions import actions_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = 'je_suis_un_tricheur'
app.config['TEMPLATES_AUTO_RELOAD'] = True

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # S'assurer que cela pointe vers la fonction de connexion correcte

# Simuler une base de données pour les utilisateurs
users = {
    "juror": {"password": generate_password_hash("juror_password"), "role": "juror"},
    "president": {"password": generate_password_hash("president_password"), "role": "president"}
}

class User(UserMixin):
    def __init__(self, username, role):
        self.id = username
        self.role = role

@login_manager.user_loader
def load_user(username):
    user_info = users.get(username)
    if user_info:
        return User(username, user_info["role"])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_info = users.get(username)
        if user_info and check_password_hash(user_info['password'], password):
            user = User(username, user_info['role'])
            login_user(user)
            flash('Connexion réussie!', 'success')
            return redirect(url_for('actions.dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#@app.route('/dashboard')
#@login_required
#def dashboard():
#    return render_template('dashboard.html')

app.register_blueprint(actions_bp)  # Assurez-vous que le Blueprint est enregistré

if __name__ == '__main__':
    app.run(debug=True)
