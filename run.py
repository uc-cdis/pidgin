from pidgin.app import app

app.config['API_URL'] = 'https://localhost/v0/submission/graphql/'
app.run('127.0.0.1', 5000, debug=True)
