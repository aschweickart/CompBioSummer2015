#!/usr/local/bin/python

from flask import Flask, request, render_template, send_from_directory, Markup
from werkzeug import secure_filename
from werkzeug.debug import DebuggedApplication
import subprocess
import os
#from flask_bootstrap import Bootstrap
from wsgiref.handlers import CGIHandler
app = Flask(__name__)
#Bootstrap(app)
UPLOAD_FOLDER = "/Users/Annalise/GitHub/CompBioSummer2015/svgFiles/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/index')
def index():
  """ Returns the index page"""
  return render_template('dtlindex.html', page='home')

@app.route('/form')
def form():
  """Returns the form page"""
  return render_template('formDTLRnB.html', page='upload')

@app.route('/documentation')
def documentation():
  """Returns the documentation page"""
  return render_template('dtldocumentation.html')

@app.route('/results')
def results():
  """Returns the results page"""
  return render_template('results.html')

@app.route('/reconcile', methods = ['GET', 'POST'])
def reconcile(carousel = None):
  """ Creates the results page using MasterReconciliation and vistrans"""
  if request.method == 'POST':
    file = request.files['newick']
    if file:
      filename = secure_filename(file.filename)
      Name = filename[:-7]
      os.mkdir(Name)
      with open(filename, "w+") as f:
         f.write(file.read())
      f.close()
      os.system("mv "+filename+" "+Name)
    else: return render_template("dtldocumentation.html")
    if request.form['dup'] != '':
      Dup = request.form['dup']
    else: Dup = 2
    if request.form['trans'] != '':
      Trans = request.form['trans']
    else: Trans = 3
    if request.form['loss'] != '':
      Loss = request.form["loss"]
    else: Loss = 1

    if request.form['switchhigh'] != '':
      switchHi = request.form['switchhigh']
    else: switchHi = 4.5

    if request.form['switchlow'] != '':
      switchLo = request.form['switchlow']
    else: switchLo = 1.5

    if request.form['losshigh'] != '':
      lossHi = request.form['losshigh']
    else: lossHi = 3

    if request.form['losslow'] != '':
      lossLo = request.form['losslow']
    else: lossLo = 1
    path2files = Name + '/' + Name
    os.system("python MasterReconciliation.py "+\
        path2files + ".newick"+" "+str(Dup)+" "+str(Trans)+" "+str(Loss)+" "+str(request.form["scoring"])+\
        " "+str(switchLo)+" "+str(switchHi)+" "+str(lossLo)+" "+str(lossHi))
    os.system('python reconConversion.py '+\
        path2files + ".newick"+" "+ str(Dup)+" "+str(Trans)+" "+str(Loss)+\
        " "+str(request.form['scoring'])+" "+str(switchLo)+" "+str(switchHi)+" "+str(lossLo)+\
        " "+str(lossHi))
  
    with open(path2files + "freqFile.txt") as f:
     lines = f.readlines()
    scoreList = string2List(lines[0])
    totalFreq = float(lines[1][:-2])
    totalRecon = float(lines[3])
    totalCost = float(lines[2][:-2])
    if request.form['scoring'] == "Frequency":
      scoreMethod = "Frequency"
    elif request.form['scoring'] == "xscape":
      scoreMethod = "Xscape Scoring"  
    else: scoreMethod = "Unit Scoring"
    carouselstr = ""
    carouselcap= ""   
    staticString = "<h4>Duplication Cost:" + str(Dup) + ", Transfer Cost: " + \
    str(Trans) + ", Loss Cost: " + str(Loss) + "<br>Maximum Parsimony Cost: " + \
    str(totalCost) +  "<br>Your scoring method: " + scoreMethod + ", Total Sum" + \
    " of Scores: " + str(totalFreq) + "<br>Total Number of Optimal " + \
    "Reconciliations: " + str(totalRecon) + "</h4>"
    for x in range(len(scoreList)):
      os.system("python vistrans.py -t " + path2files + ".tree -s " +
      path2files + str(x) + ".stree -b " + path2files + str(x) + ".mowgli.brecon -o " + \
      path2files +  str(x) + ".svg")
      
      score = scoreList[x]
      percent = 100.0*score/totalFreq
      if x ==0:
        runningTot = percent 
      
        carouselstr +='<li data-target="#results" data-slide-to="0" ' + \
        'class="active"></li>' + "\n"
    
        carouselcap +="<div class='item active'><img src='/uploads/" +  Name + \
        str(x) + ".svg' alt='First slide' width='460' height='345'>" +  \
          "<div class='carousel-caption'><font color='black'><h3>" + \
          "Reconciliation 1 of " + str(len(scoreList)) + "</h3><p>Score = " + \
          str(score) + "<br>Percent of total = " + str(percent) + "%<br>Running" + \
          " total = " + str(runningTot) + "%</font></p></div></div>" + "\n"
      
        os.system("cp " + str(path2files) + str(x) + '.svg ' + UPLOAD_FOLDER)
      else:
        runningTotScore = runningTotal(scoreList, x)
        runningTot = 100.0*runningTotScore/totalFreq
        if runningTot > 100:
          runningTot = 100
        carouselstr +='<li data-target="#results" data-slide-to="' + str(x) + \
        '"></li>' + "\n"
        carouselcap +="<div class='item'><img src='/uploads/" +  Name + str(x) + \
        ".svg' alt='First slide' width='460' height='345'>" + \
         "<div class='carousel-caption'><font color='black'><h3>" + \
         "Reconciliation " + str(x + 1) + " of " + str(len(scoreList)) + \
         "</h3><p>Score = " +  str(score) + " <br>Percent of total = " + \
         str(percent) + "%<br>Running total = " + str(runningTot) + \
         "%</font></p></div></div>" + "\n"
        os.system("cp " + path2files +  str(x) + '.svg ' + UPLOAD_FOLDER)
  staticString = Markup(staticString)
  carouselstr = Markup(carouselstr)
  carouselcap = Markup(carouselcap)
  #os.system("rm -r " + Name)
  return render_template("results.html", carouselstr = carouselstr, \
    carouselcap = carouselcap, staticString = staticString)
    
        
def runningTotal(scoresList, index):
  """Takes in a list of scores and an integer, index, and returns the sum of
  the list's entries up to that index"""
  runningTot = 0
  for n in range(len(scoresList)):
    if n<=index:
      runningTot += scoresList[n]   
  return runningTot
    
def string2List(string):
  """Takes in a string of a list and returns the list"""
  newString = string.strip('[')
  newerString = newString.strip(']\n')
  stringList = newerString.split(',') 
  for n in range(len(stringList)):
    stringList[n] = float(stringList[n])
  return stringList
    
    
@app.route('/uploads/<filename>')
def send_file(filename):
  """Takes in a filename and sends it from the directory to the results page"""
  return send_from_directory(UPLOAD_FOLDER, filename )
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
app.debug = True
app.run()

