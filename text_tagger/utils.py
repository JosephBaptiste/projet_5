import re
import pickle

from PIL import Image
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier

# Les objets qui ne sont pas liés à Flask

def get_model():
	"""
	model est un multioutputclassifier.
	Il faut utiliser le tfidf vectorizer sur les données avant de les passer dans le modèle.
	le mlb multilabel binarizer est utile pour changer l'output en tags.
	"""
	with open('./static/model.pkl', 'rb') as f:
		clf = pickle.load(f)
	with open('./static/tfidfvectorizer.pkl','rb') as f:
		tfidf = pickle.load(f)
	with open('./static/mlb.pkl','rb') as f:
		mlb = pickle.load(f)
	return clf, tfidf, mlb

def use_model(input: str=None):
	"""
	Fonction utilisée sur un titre pour une 
	première prédiction.
	"""
	if not input:
		return False
	model, tfidf_vectorizer, mlb = get_model()
	data_input = tfidf_vectorizer.transform([input])
	y_pred = model.predict(data_input)
	result = [[x for x, y in zip(mlb.classes_, z) if y] for z in y_pred][0]
	return " ".join(result)

def get_tag(title: str=None, tags: str=None):
	"""
	Fonction utilisée pour ajouter un tag, à une 
	prédiction déjà réalisée.
	"""
	if len(tags) > 1:
		tags_liste = str.split(tags, " ")
	elif len(tags) == 1:
		tags_liste = [tags]
	else:
		tags_liste = []
	model, tfidf_vectorizer, mlb = get_model()
	data_input = tfidf_vectorizer.transform([title])
	y_pred_proba = [x[0].squeeze()[1] for x in model.predict_proba(data_input)]
	dic_probas = dict(zip(mlb.classes_, y_pred_proba))
	while len(dic_probas.keys()) > 0:
		tag_temp = max(dic_probas, key=dic_probas.get)
		dic_probas.pop(tag_temp, None)
		if not tag_temp in tags_liste:
			return tag_temp
		else:
			pass
	return ''