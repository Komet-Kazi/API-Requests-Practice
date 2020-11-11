# /my_app/hello/models.py - has a non persistant key-value store

# We have used a very simple non-persistent in-memory key-value store for the demonstration of the model layout structure.
# It is true that we could have written the dictionary for the MESSAGES hash map in views.py
# but it's best practice to keep the model and view layers separate.


MESSAGES = {
    'default': 'Hello to the World of Flask!',
}