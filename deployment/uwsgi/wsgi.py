from pidgin.app import app

# wsgi.ini references this file

config = app.config

print("wsgi.py")

config['API_URL'] = 'http://peregrine-service/v0/submission/graphql/'
application = app
