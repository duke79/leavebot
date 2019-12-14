from . import app

@app.route('/')
def hello_world():
    return 'Flask Dockerized and deployed to Heroku'