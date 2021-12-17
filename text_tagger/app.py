from flask import Flask, render_template


# contient le code python réel qui importera l'application et démarrera le serveur de développement).
app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

if __name__ == "__main__":
    app.run()