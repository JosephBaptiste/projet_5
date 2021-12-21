# Les routes sont définies ici
from flask import Flask

from utils import testfunc

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/')
def index():
        return "Hello world !"

@app.route('/contents/<int:content_id>/')
def content(content_id):
    return content_id

if __name__ == "__main__":
        app.run()