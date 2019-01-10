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
boardListParser.add_argument('board_name', type=str, help='Name of your board')
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
        args = boardListParser.parse_args()
        board = self.addBoard(args['board_name'])
        retval = (board, 201) if board else ({'error':'Bad input'}, 400)#placeholder error code
        return retval

class Board(Resource, boards_handler):
    '''
        Retrieve a single board using GET
    '''
    def get(self, boardId):
        return self.getBoard(boardId)
        
    '''
        Rename a board via PUT
    '''
    def put(self, boardId):
        args = boardListParser.parse_args()
        self.updateBoard(boardId, args['board_name'])
        return db.getBoard(boardId)

api.add_resource(BoardList,'/Boards')
api.add_resource(Board,'/Boards/<int:boardId>')

'''
    Rename, listall
    
    Child of Boards
'''
class Labels(Resource):
    pass
    
'''
    Create, rename, archive, reorder, listall, individual
    
    Child of Boards
'''
class Lists(Resource):
    pass
    
'''
    Create, rename, archive, reorder, move, assignmember, assignlabels, listall, individual
    
    Child of Lists
'''
class Cards(Resource):
    pass
    
'''
    Create, rename, archive, listall, individual
    
    Child of Boards
'''
class Members(Resource):
    pass



if __name__ == '__main__':
    app.run()
