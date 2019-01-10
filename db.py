import sqlite3
import sys, threading

class db_handler:
    #define the constructor
    def __init__(self):
        self.connection = sqlite3.connect('project.db')

    #and now the destructor
    def __del__(self):
        self.connection.commit()
        self.connection.close()

    #takes in cols as (col1, col2, ..., coln) and a single table
    #returns a list of rows, represented as dicts accessible by return[rowNum]['coln']
    def basic_query(self, table, cols):
        queryString = "SELECT " + ", ".join(cols) + " FROM " + table
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
     @param kwargs is a dictionary with the SQL attributes paired to
            the values for an instance of the object to be inserted

     @return True if successful, False is an error is encountered
    '''
    def insert_query(self, tablename, **kwargs):
        keys = ["%s" % k for k in kwargs.keys()]
        values = ["'%s'" % v for v in kwargs.values()]
        query = list()
        query.append("INSERT INTO %s (" % tablename)
        query.append(", ".join(keys))
        query.append(") VALUES (")
        query.append(", ".join(values))
        query.append(")")
        query = "".join(query)

        cursor = self.getCursorHandler()
        try:
            sys.stderr.write(query + "\n")
            cursor.execute(query)
            
        # If there's an error, print it to notify that the insert failed
        except sqlite3.Error as e:
            sys.stderr.write("Database error: " + e.args[0])
            return False
        return True

    # Generates an ID for a record by incrementing up one from the last ID
    # in the table.
    def generate_id(self,tablename):
        # Generate the query to get the largest ID
        max_ID_query = "SELECT COUNT (*)\nFROM "+tablename
        cursor = self.getCursorHandler()
        # Return the maximum ID plus one
        cursor.execute(max_ID_query)
        return cursor.fetchone()[0] + 1

    '''
    General function for updating rows in a table
    @param table is the database table to be updated
    @param dictSet is a dictionary of attributes to be set mapped to corresponding values
    @param dictWhere is a dictionary of attributes mapped to values that will choose the item to set

    @return True if successful, False if an error is encountered
    '''
    def update_query(self, table, dictSet, dictWhere):
        query = "UPDATE " + table
        
        # Append set
        query += " SET "
        query += ", ".join(" = ".join(item) for item in dictSet.items())
        
        # Append where
        query += " WHERE "
        query += " AND ".join(" = ".join(item) for item in dictWhere.items())
        
        sys.stderr.write(query + '\n')

        cursor = self.getCursorHandler()
        try:
            cursor.execute(query)
        # If there's an error, print the error and notify that the insert failed
        except sqlite3.Error as e:
            sys.stderr.write("Database error: " + e.args[0])
            return False
        return True



    def matched_query(self, table, cols, dictWhere):
        query = "SELECT " + ", ".join(cols) + " FROM " + table + " WHERE "
        query += " AND ".join(" = ".join(item) for item in dictWhere.items())
        #sys.stderr.write(query + '\n')
        cursor = self.getCursorHandler()
        cursor.execute(query)
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
        #cancel any remaining timer on cleanup
        try:
            self.t.cancel()
        except NameError:
            pass
        self.cursor.close()

    def execute(self, query):
        self.t = threading.Timer(3.0, self.connection.interrupt)
        self.t.start()
        #sys.stderr.write("DEBUG: connection to the database for querying will only last 3 seconds\n")
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
        boardList = self.basic_query('boards', ('board_id','board_name'))
        return boardList

    def addBoard(self, boardName, **kwargs):
        id = self.generate_id('boards')
        success = self.insert_query('boards',
            board_id = str(id),
            board_name = boardName,
            **kwargs
        )#no response to errors yet, add this in later
        retval = id if success else False
        return retval
        



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