# stitch_api

This is not a complete project, however I believe it demonstrates my coding
style effectively and with the following caveats:
 - Attention has been paid to the BoardList and Board classes in index.py, as
   well as the entirety of db.py in order to demonstrate my typical attention to
   detail
 - Module layouts are in my typical coding style, however documentation is
   scarce due to time limitations, and shown most effectively in db.py
 - I have done my best to make the output of the BoardList and Board classes as
   RESTful as I know how to on short notice. If I took more time, I could learn
   the full methodology and then be set for future API designs :)
 - I used an sqlite database for to avoid the need to host a MySQL database for
   the prototype, however this database code has been used on Oracle databases
   in the past. Thanks to Python's common interfaces, it's portable!
   
Dependencies:
 - flask
 - flask_restful
 - pipenv