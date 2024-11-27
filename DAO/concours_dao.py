from typing import Optional

from .dao import Dao
from ..concours import selection


class SelectionDao(Dao):
    def create(self, obj: selection) -> int:
        """Crée l'entité en BD correspondant à l'objet obj
        :param obj: à créer sous forme d'entité en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        query = '''INSERT 
        INTO selection (stage, book_id, vote)
        VALUES (%s, %s, %s)''' % (obj.stage,
                                  obj.book_id,
                                  obj.vote,)
        with self.__class__.connection.cursor() as cursor:
            cursor.execute(query)
            last_inserted_id = cursor.lastrowid
            cursor.fetchall()
            self.__class__.connection.commit()
            return last_inserted_id


    def read(self, id_entity: int) -> Optional[selection]:
        """Renvoie l'objet correspondant à l'entité dont l'id est id_entity
           (ou None s'il n'a pu être trouvé)"""
        query = '''SELECT * 
                   FROM selection 
                   WHERE id = %s'''  # Placeholder sécurisé

        with self.__class__.connection.cursor() as cursor:
            cursor.execute(query, (id_entity,))  # Exécution avec le paramètre sécurisé
            resultat = cursor.fetchone()  # Récupération d'un seul résultat

            # Initialisation de la variable avec le type Optional
            resultat_selection: Optional[selection] = None

            if resultat:
                resultat = dict(resultat)
                resultat_selection = selection(
                    s_id=resultat.get('id'),
                    stage=resultat.get('stage'),
                    book_id=resultat.get('book_id'),
                    vote=resultat.get('vote')
                )

        return resultat_selection

    def update(self, obj: selection) -> bool:
        """Met à jour en BD l'entité correspondant à obj, pour y correspondre

        :param obj: objet déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        query = '''UPDATE selection
        SET id = %s, stage = %s, book_id = %s, vote = %s
        WHERE id = %s'''
        params = (obj.s_id, obj.stage, obj.book_id, obj.vote, obj.s_id,)
        with self.__class__.connection.cursor() as cursor:
            effet = cursor.execute(query, params)
            self.__class__.connection.commit()
        if not effet:
            return False
        elif effet == 1:
            return True
        else:
            print(f"Panique : {effet} lignes affectées")

    def delete(self, obj: selection) -> bool:
        """Supprime en BD l'entité correspondant à obj"""

        query = '''DELETE FROM `selection` 
                   WHERE id = %s 
                   AND stage = %s
                   AND book_id = %s'''

        # Paramètres pour la requête
        params = (obj.s_id, obj.stage, obj.book_id)

        print(f"Exécution de la suppression avec paramètres : {params}")

        with self.__class__.connection.cursor() as cursor:
            effet = cursor.execute(query, params)
            self.__class__.connection.commit()

        if effet == 0:
            print("Aucune ligne supprimée.")
            return False
        elif effet == 1:
            print("Suppression réussie.")
            return True
        else:
            print(f"Panique : {effet} lignes affectées")
            return False

    def palmares(self, choix: int):
        requete = '''SELECT Livre.id, Livre.titre, 
        auteur.name, auteur.surname 
        FROM selection 
        INNER JOIN Livre on Livre.id = selection.book_id 
        INNER JOIN auteur on Livre.id_auteur = auteur.id 
        WHERE selection.stage = %d''' % choix
        with self.__class__.connection.cursor() as cursor:
            cursor.execute(requete)
            resultat = cursor.fetchall()
            return resultat

    def digest(self, ident):
        requete = '''SELECT digest 
                    FROM Livre
                    WHERE id = %s ''' % ident
        with self.__class__.connection.cursor() as cursor:
            cursor.execute(requete)
            resultat = cursor.fetchone()
            resultat = dict(resultat)
            cursor.fetchall()
        return resultat.get('digest')

    def cv(self, ident):
        requete = '''SELECT cv 
                            FROM auteur
                            INNER JOIN Livre
                            ON Livre.id_auteur = auteur.id
                            WHERE Livre.id = %s ''' % ident
        with self.__class__.connection.cursor() as cursor:
            cursor.execute(requete)
            resultat = cursor.fetchone()
            cursor.fetchall()
            resultat = dict(resultat)
        return resultat.get('cv')

    def get_sel_id(self, stage: int, book_id: int):
        query = f'''SELECT id 
        FROM selection 
        WHERE stage = {stage}
        AND book_id = {book_id}'''
        with self.__class__.connection.cursor() as cursor:
            cursor.execute(query)
            resultat = cursor.fetchone()
            cursor.fetchall()
            resultat = dict(resultat)
        return resultat.get('id')
