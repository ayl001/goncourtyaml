from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .DAO.concours_dao import SelectionDao
from .concours import selection

actions_bp = Blueprint('actions', __name__)

@actions_bp.route('/dashboard')  # Définition de la route
def dashboard():
    if current_user.is_authenticated:
        if current_user.role == "president":
            return render_template('president_dashboard.html')
        elif current_user.role == "juror":
            return render_template('juror_dashboard.html')
    return render_template('peone_dashboard.html')

@actions_bp.route('/choisir_selection', methods=['GET', 'POST'])
def choisir_selection():
    if request.method == 'POST':
        stage = int(request.form.get('stage', 0))  # Récupération de la sélection depuis le formulaire
        my_selection = SelectionDao()  # Instance de la classe pour gérer les sélections
        resultat = my_selection.palmares(choix=stage)  # Récupération des résultats pour la sélection choisie
        return render_template('selection_result.html', resultat=resultat, stage=stage)  # Affiche les résultats
    return render_template('choisir_selection.html')

@actions_bp.route('/vote', methods=['POST'])
@login_required
def juror_vote():
    if current_user.role == "juror":
        book_id = request.form.get('book_id')  # Assurez-vous que 'book_id' est bien envoyé
        stage = request.form.get('stage')

        flash(f"j'entre dans vote, book_id = {book_id} \n"
              f"étape = {stage} ")
        my_sel = SelectionDao()
        selection_obj = my_sel.read(book_id)  # Essayez de récupérer l'objet sélection

        if selection_obj is None:
            flash('Erreur: Sélection introuvable.', 'danger')
            return redirect(url_for('actions.choisir_selection'))  # Redirection en cas d'erreur

        # Incrémentez le vote
        selection_obj.vote += 1
        print("I increment the vote")
        flash(f"vote vaut {selection_obj.vote}")

        # Mettez à jour l'objet dans la base de données
        if my_sel.update(selection_obj):
            flash('Vote enregistré avec succès!', 'success')
        else:
            flash('Erreur: Échec de la mise à jour du vote.', 'danger')

        return redirect(url_for('actions.choisir_selection'))  # Redirigez après l'opération
    return "Accès refusé", 403


@actions_bp.route('/get_bio/<int:book_id>', methods=['GET'])
def get_bio(book_id):
    sel = SelectionDao()  # Créez une instance de votre DAO
    bio = sel.cv(book_id)  # Récupère la biographie avec l'ID du livre

    if bio:
        return render_template('bio.html', bio=bio)  # Rendre le template avec la biographie
    else:
        return "Biographie non trouvée", 404  # Gérer le cas où aucune biographie n'est trouvée

@actions_bp.route('/get_digest/<int:book_id>', methods=['GET'])
def get_digest(book_id):
    sel = SelectionDao()  # Créez une instance de votre DAO
    digest = sel.digest(book_id)  # Récupère le résumé avec l'ID du livre

    if digest:
        return render_template('digest.html', digest=digest)  # Rendre le template avec le résumé
    else:
        return "Résumé non trouvé", 404  # Gérer le cas où aucun résumé n'est trouvé

@actions_bp.route('/add_selection', methods=['POST'])
@login_required
def add_selection():
    if current_user.role == "president":
        book_id = request.form.get('book_id')
        stage = request.form.get('stage')
        nouvelle_selection = selection(s_id=0,
                                       stage= f"{int(stage) + 1}",
                                       book_id=book_id,
                                       vote=0)
        commis = SelectionDao()
        commis.create(nouvelle_selection)
        flash('Sélection ajoutée!', 'success')
        return redirect(url_for('actions.dashboard'))
    return "Accès refusé", 403
