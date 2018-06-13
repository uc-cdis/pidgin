from pidgin.app import app

app.config['API_URL'] = 'https://pauline.planx-pla.net/api/v0/submission/graphql/'
app.run('127.0.0.1', 5000, debug=True)
