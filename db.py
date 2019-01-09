'''
Temporary in-memory structures to get the API functioning before integrating
a MySQL or sqlite database. There is no persistence here, it's just to get the
basics going!
'''
boardDicts = {1:{
    'lists':{
        '1':{
            'cards':{
                '1':{
                    'title':'Test Card',
                    'description':'A test card',
                    'duedate':'placeholder',
                    'label':None,
                    'members':[]
                }
            }
        }
    },
    'members':None
}}

def getBoards():
    return boardDicts

def addBoard(boardName):
    id = len(boardDicts.keys())+1
    boardDicts[id] = {
        'name':boardName,
        'lists':{
            '1':{
                'title':'Default List',
                'cards':{}
                }
        },
        'members':None
    }
    return boardDicts[id]