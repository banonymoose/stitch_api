from db import *

db = db_handler()

print(db.basic_query(('board_id', 'board_name','label1'), 'boards'))

id = db.generate_id('boards')
db.insert_query('boards',
    board_id=str(id),
    board_name='board{}'.format(id),
    label1='test1',
    label2='test2',
    label3='test3',
    label4='test4',
    label5='test5',
    label6='test6'
)

print(db.basic_query(('board_id', 'board_name','label1'), 'boards'))

del db