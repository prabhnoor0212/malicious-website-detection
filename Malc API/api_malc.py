import flask
from flask import Flask, request, render_template
from sklearn.externals import joblib
import numpy as np
import impFuncs

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return flask.render_template('index.html')


@app.route('/predict', methods=['POST'])
def make_prediction():

	if request.method=='POST':

		url = request.form.get('url')

		subdomains = (impFuncs.checkSubdomains(url)-2.776)/0.785
		ssl = impFuncs.checkSSL(url)
		ssle = (int(ssl[0])-223.691)/456.308
		redir = impFuncs.hasDoubleSlashes(url)
		anchors = (impFuncs.checkAnchors(url)-215.224)/90.402
		svform = impFuncs.checkServerForm(url)

		print(subdomains, anchors, svform, ssle, ssl[1], redir)

		prediction = model.predict([[subdomains, anchors, svform, ssle, ssl[1], redir]])

		label = str(np.squeeze(prediction))
		
		return render_template('index.html', label=label)

if __name__ == '__main__':

	#model = joblib.load('classifier2.pkl')
	app.run(host='0.0.0.0', port=8000, debug=True)