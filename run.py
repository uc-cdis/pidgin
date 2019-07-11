from pidgin.app import app

app.config["API_URL"] = "http://localhost/v0/submission/graphql/"  # peregrine endpoint
app.config["API_HEALTH_URL"] = "http://localhost/_status"
app.run("127.0.0.1", 5000, debug=True)
