# stitch_api

This is not a complete project, however I believe it demonstrates my coding
style effectively! Flask is an extremely lean library, and I spent a lot of time
reinventing the wheel (which I'm sure will be much less of a concern once I gain
experience with Django and other libraries which handle the minutiae like
linking and pagination)

General notes:
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
 - Total time spent has been approximately 10-12 hours, including debugging time
   and time spent researching how to design a REST API as opposed to just
   using one!
   
Dependencies:
 - flask (if pipenv not used)
 - flask_restful (if pipenv not used)
 - pipenv

Run it with `pipenv run python index.py`, then use curl to interact