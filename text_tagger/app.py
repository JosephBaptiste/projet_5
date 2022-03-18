import sys

from flask import Flask, render_template, url_for, request, redirect
from flask import session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from utils import use_model, get_tag

# contient le code python réel qui importera l'application et démarrera le serveur de développement).
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Resultats(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	tags = db.Column(db.String(200), nullable=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return'<Tag %r>' % self.id


@app.route("/", methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		title = request.form['title']
		tags = use_model(title)
		tags = tags + " " + get_tag(title, tags)
		new_result = Resultats(title=title, tags=tags)
		try:
			db.session.add(new_result)
			db.session.commit()
			return redirect('/')
		except:
			return 'Problème ajout des données'
	else:
		resultats = Resultats.query.order_by(Resultats.date_created).all()
		return render_template('index.html', resultats=resultats)

@app.route('/delete/<int:id>')
def delete(id):
	result_to_delete = Resultats.query.get_or_404(id)
	try:
		db.session.delete(result_to_delete)
		db.session.commit()
		return redirect('/')
	except:
		return 'Problème lors de la suppression'

@app.route('/add_tag/<int:id>')
def add_tag(id):
	resultat = Resultats.query.get_or_404(id)
	new_tag = get_tag(resultat.title, resultat.tags)
	resultat.tags = resultat.tags + " " + new_tag
	try:
		db.session.commit()
		return redirect('/')
	except:
		return 'Problème lors de la modification'

if __name__ == "__main__":
    app.run(debug=True)
    #app.run()