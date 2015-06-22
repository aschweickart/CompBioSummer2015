#!/usr/local/bin/python

from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename
import MasterReconciliation
import os


app = Flask(__name__)


@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/form')
def form():
	return render_template('form.html')

@app.route('/reconcile', methods = ['GET', 'POST'])
def reconcile():
	if request.method == 'POST':
		file = request.files['newick']
		Dup = request.form['dup']
		Trans = request.form['trans']
		Loss = request.form["loss"]
		K = request.form['k']
		if file:
			filename = secure_filename(file.filename)
			Name = filename[:-7]
			file.save('/Users/Annalise/Desktop/k-best/'+filename)
			os.system("python MasterReconciliation.py "+filename+" "+Dup+" "+Trans+" "+Loss+" "+K)
			for x in range(K):
				os.system("./tree\ and\ smap\ files/vistrans -t "+Name+".tree -s "+Name+".stree -b "+Name+x+".mowgli.brecon -o "+Name+".svg")
	return render_template('form.html')
if __name__ == "__main__":
	app.run()