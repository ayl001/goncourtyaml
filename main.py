import concours
from DAO.concours_dao import SelectionDao

import actions

my_selection: SelectionDao = SelectionDao()
ids = 10
Test: concours.selection = my_selection.read(ids)
if Test:
    print('selection_id : %d \n' % Test.s_id,
          'étape %d \n' % Test.stage,
          'Livre %d \n' % Test.book_id,
          'Vote %d \n' % Test.vote)
else:
    print( 'la sélection %d n\'existe pas' % ids )
my_peone=actions.peone()
my_peone.choisir_selection()
print('et c\'est toujours %s' % my_peone.choix)
my_selection = SelectionDao()
my_selection.palmares(my_peone.choix)


