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

		ssl = impFuncs.checkSSL(url)
		isIP = impFuncs.isIpAddress(url)
		hasHTTPS = impFuncs.checkHTTPSinURL(url)
		redir = impFuncs.hasDoubleSlashes(url)
		anchors = impFuncs.checkAnchors(url)
		svform = impFuncs.checkServerForm(url)
		ssl[0] = ((int(ssl[0]) - 223.7) / 456.3)

		print(isIP, anchors, svform, ssl[0], ssl[1], redir, hasHTTPS)

		prediction = model.predict([[isIP, anchors, svform, ssl[0], ssl[1], redir, hasHTTPS]])

		label = str(np.squeeze(prediction))
		
		return render_template('index.html', label=label)

if __name__ == '__main__':

	model = joblib.load('classifier3.pkl')
	app.run(host='0.0.0.0', port=8000, debug=True)