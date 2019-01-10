from db import *

db = db_handler()

data = db.basic_query(('board_id', 'board_name','label1','label2'), 'boards')

print(data)

del db