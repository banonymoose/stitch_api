import sqlite3
import sys, threading

class db_handler:
    #define the constructor
    def __init__(self):
        self.connection = sqlite3.connect('project.db')

    #and now the destructor
    def __del__(self):
        self.connection.close()

    #takes in cols as (col1, col2, ..., coln) and a single table
    #returns a list of rows, represented as dicts accessible by return[rowNum]['coln']
    def basic_query(self, cols, table):
        queryString = "select " + ", ".join(cols) + " from " + table
        #sys.stderr.write(queryString + '\n')
        cursor = cursor_handler(self.connection)
        cursor.execute(queryString)
        rows = cursor.fetchall()
        results = []
        for row in rows:
            #sys.stderr.write(row + '\n')
            resultDict = {}
            for colNum, value in enumerate(row):
                resultDict[cols[colNum]] = value
            results.append(resultDict)
        return results


    '''
     General function for inserting into a table.
     Takes the name of the table and insert the attributes and values
     stored in a dictionary.
     @param tablename is a string with the name of the table in the database
     @param attrToValuesDict is a dictionary with the SQL attributes paired to
            the values for an instance of the object to be inserted

     @return a string indicating the error if it failed, or succeeded.
    '''
    def insert_object(self, tablename, attrToValuesDict):

        kwargs = attrToValuesDict

        cursor = self.getCursorHandler()
        try:
            sys.stderr.write(self.insert_query(tablename, **kwargs) + "\n")
            cursor.execute(self.insert_query(tablename, **kwargs))
        # If there's an error, print the error and notify that the insert failed
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            return str(error.code)+": "+ str(error.message)+"\n"+str(error.context)+"\nInsert failed."
        # If the try worked it should return a success message
        return "Insert "+tablename+" successful."

    '''
    Generates an INSERT INTO query to be executed for general cases.
    @param table is the name of the table to be inserted into
    @param **kwargs is a dictionary of attribute names : values for an instance of the object

    @return a string query to be executed
    '''
    def insert_query(self, table, **kwargs):
        keys = ["%s" % k for k in kwargs]
        values = ["'%s'" % v for v in kwargs.values()]
        query = list()
        query.append("INSERT INTO %s (" % table)
        query.append(", ".join(keys))
        query.append(")VALUES (")
        query.append(", ".join(values))
        query.append(")")
        return "".join(query)

    # Generates an ID for an object by incrementing up one from the last ID
    # in the table.
    def generate_id(self,tablename):
        # Generate the query to get the largest ID
        max_ID_query = "SELECT count(*)\nFROM "+tablename
        cursor = self.getCursorHandler()
        # Return the maximum ID plus one
        cursor.execute(max_ID_query)
        return cursor.fetchone()[0] + 1

    '''
    Generates an UPDATE query to be executed for general cases.
    @param table is the database table to be updated
    @param dictSet is a dictionary of attributes to be set mapped to corresponding values
    @param dictWhere is a dictionary of attributes mapped to values that will choose the item to set

    @return an update query to be executed
    '''
    def update_query(self, table, dictSet, where):
        query = "UPDATE " + table + " SET "
        setKeys = ["%s" % k for k in dictSet]
        setVals = ["'%s'" % v if isinstance(v, str) else "%s" % v for v in dictSet.values()]
        # Append set
        for n in range(len(setKeys)):
            query += setKeys[n] + " = " + setVals[n]
            if n != len(setKeys) - 1:
                query += ", "
        # Append where
        query += " WHERE " + where

        cursor = self.getCursorHandler()
        try:
            cursor.execute(query)
        # If there's an error, print the error and notify that the insert failed
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            return error.code + ": " + error.message + "\n" + error.context + "\nInsert failed."

        return "Update " + table + " successful."



    def matched_query(self, cols, table, match):
        queryString = "select " + ", ".join(cols) + " from " + table + " where " + match
        #sys.stderr.write(queryString + '\n')
        cursor = self.getCursorHandler()
        cursor.execute(queryString)
        rows = cursor.fetchall()
        results = []
        for row in rows:
            #sys.stderr.write(row + '\n')
            resultDict = {}
            for colNum, value in enumerate(row):
                resultDict[cols[colNum]] = value
            results.append(resultDict)
        return results

    def getCursorHandler(self):
        return cursor_handler(self.connection)

class cursor_handler:
    #define the constructor
    def __init__(self, db_connection):
        self.cursor = db_connection.cursor()
        self.connection = db_connection

    #and now the destructor
    def __del__(self):
        self.cursor.close()

    def execute(self, query):
        self.t = threading.Timer(3.0, self.connection.cancel)
        self.t.start()
        sys.stderr.write("DEBUG: connection to the database for querying will only last 3 seconds\n")
        self.cursor.execute(query)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

class boards_handler(db_handler):
    def __init__(self):
        db_handler.__init__(self)

    def __del__(self):
        db_handler.__del__(self)
        
    def getBoards(self):
        boardList = self.basic_query(("id","name"), "boards")
        return boardList






"""
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
"""