from flask import Flask, render_template, url_for, redirect, request, session
from flask_restful import Resource, Api, reqparse
from db import *
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'thisIsNotVerySecure'
api = Api(app)

global_db = db_handler()

'''
    Create, rename, archive, listall, individual
'''
boardListParser = reqparse.RequestParser()
boardListParser.add_argument('board_id', type=int, help='ID of the board')
boardListParser.add_argument('board_name', type=str, help='Name of the board')
boardListParser.add_argument('label1', type=str, help='Card label 1')
boardListParser.add_argument('label2', type=str, help='Card label 2')
boardListParser.add_argument('label3', type=str, help='Card label 3')
boardListParser.add_argument('label4', type=str, help='Card label 4')
boardListParser.add_argument('label5', type=str, help='Card label 5')
boardListParser.add_argument('label6', type=str, help='Card label 6')

class BoardList(Resource, boards_handler):
    '''
        Retrieve list of boards using GET
    '''
    def get(self):
        return self.getBoards()
        
    '''
        Create a new board using POST
    '''
    def post(self):
        restArgs = boardListParser.parse_args()
        addArgs = {}
        for i in range(1,7):
            label = 'label{}'.format(i)
            if label in restArgs: addArgs[label] = restArgs[label]
        #for item in restArgs.items(): sys.stderr.write('{}, {}\n'.format(item[0],item[1]))
        board = self.addBoard(restArgs['board_name'], **addArgs)
        retval = (board, 201) if board else ({'error':'Bad input'}, 400)#placeholder error code
        return retval

class Board(Resource, boards_handler):
    '''
        Retrieve a single board using GET
    '''
    def get(self, boardId):
        return self.getBoard(boardId)#need to append links to lists
        
    '''
        Rename a board and/or labels using PUT
    '''
    def put(self, boardId):
        restArgs = boardListParser.parse_args()
        putArgs = {}
        if 'board_name' in restArgs: putArgs['board_name'] = restArgs['board_name']
        for i in range(1,7):
            label = 'label{}'.format(i)
            if label in restArgs: putArgs[label] = restArgs[label]
        #for item in restArgs.items(): sys.stderr.write('{}, {}\n'.format(item[0],item[1]))
        board = self.updateBoard(boardId, **putArgs)
        retval = (board, 200) if board else ({'error':'Bad input'}, 400)#placeholder error code
        return retval

api.add_resource(BoardList,'/Boards')
api.add_resource(Board,'/Boards/<int:boardId>')

'''
    Rename, listall
    
    Child of Boards
'''
class Labels(Resource):
    pass#Functionality included in board handling
    
'''
    Create, rename, archive, reorder, listall, individual
    
    Child of Boards
'''
listsParser = reqparse.RequestParser()
listsParser.add_argument('list_id', type=int, help='ID of the list')
listsParser.add_argument('list_name', type=str, help='Name of the list')

class Lists(Resource, lists_handler):
    def get(self, boardId):
        return self.getLists(boardId)
        
    def post(self, boardId):
        restArgs = listsParser.parse_args()
        #for item in restArgs.items(): sys.stderr.write('{}, {}\n'.format(item[0],item[1]))
        list = self.addList(restArgs['list_name'], boardId)
        retval = (list, 201) if board else ({'error':'Bad input'}, 400)#placeholder error code
        return retval
        
    
class List(Resource, lists_handler):
    def get(self, listId):
        return self.getList(listId)#need to append links to cards
        
    def put(self, listId):
        restArgs = listsParser.parse_args()
        putArgs = {}
        
        if 'list_name' in restArgs: putArgs['list_name'] = restArgs['list_name']
        
        list = self.updateList(listId, **putArgs)
        retval = (list, 200) if list else ({'error':'Bad input'}, 400)#placeholder error code
        return retval
        

api.add_resource(Lists,'/Lists/<int:boardId>')
api.add_resource(List,'/Lists/<int:boardId>/<int:listId>')
    
'''
    Create, rename, archive, reorder, move, assignmember, assignlabels, listall, individual
    
    Child of Lists
'''
cardsParser = reqparse.RequestParser()
cardsParser.add_argument('card_id', type=int, help='ID of the card')
cardsParser.add_argument('description', type=str, help='Description of the card')
cardsParser.add_argument('due_date', type=str, help='Due date of the card (ISO 8601 format)')
cardsParser.add_argument('label', type=int, help='Label ID for the card')

class Cards(Resource, cards_handler):
    def get(self, listId):
        return self.getCards(listId)
        
    def post(self, listId):
        restArgs = cardsParser.parse_args()
        card = self.addCard(listId,
            description=restArgs['description'],
            duedate=restArgs['due_date'],
            label=None if 'label' not in restArgs else restArts['label']
        )
        retval = (card, 201) if card else ({'error':'Bad input'}, 400)#placeholder error code
        return retval
        
class Card(Resource, cards_handler):
    def get(self, cardId):
        return self.getCard(cardId)
        
    def put(self, cardId):
        restArgs = cardsParser.parse_args()
        putArgs = {}
        
        if 'description' in restArgs: putArgs['description'] = restArgs['description']
        if 'duedate' in restArgs: putArgs['duedate'] = restArgs['duedate']
        if 'label' in restArgs: putArgs['label'] = restArgs['label']
        
        card = self.updateCard(cardId, **putArgs)
        retval = (list, 200) if list else ({'error':'Bad input'}, 400)#placeholder error code
        return retval
    
'''
    Create, rename, archive, listall, individual
    
    Child of Boards
'''
class Members(Resource):
    pass



if __name__ == '__main__':
    app.run()
