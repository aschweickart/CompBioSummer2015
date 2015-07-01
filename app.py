from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash, Markup
from werkzeug import secure_filename
import os
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)
UPLOAD_FOLDER = '/Users/Annalise/GitHub/CompBioSummer2015/svgFiles/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/form')
def form():
  return render_template('formDTLRnB.html')

@app.route('/results')
def results():
  return render_template('results.html')  

@app.route('/reconcile', methods = ['GET', 'POST'])
def reconcile(carousel = None):
  if request.method == 'POST':
    file = request.files['newick']
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
    else: switchHi = 5

    if request.form['switchlow'] != '':
      switchLo = request.form['switchlow']
    else: switchLo = 0.1

    if request.form['losshigh'] != '':
      lossHi = request.form['losshigh']
    else: lossHi = 5

    if request.form['losslow'] != '':
      lossLo = request.form['losslow']
    else: lossLo = 0.1

    if file:
      filename = secure_filename(file.filename)
      Name = filename[:-7]
      os.system("mkdir "+Name)
      path2files = Name + '/' + Name
      svgFile = Name + "0.svg"
      file.save('/Users/Annalise/GitHub/CompBioSummer2015/'+path2files + ".newick")
      os.system("python /Users/Annalise/GitHub/CompBioSummer2015/MasterReconciliation.py "+path2files+".newick"+" "+str(Dup)+" "+str(Trans)+" "+str(Loss)+" "+str(request.form["scoring"])+" "+str(switchLo)+" "+str(switchHi)+" "+str(lossLo)+" "+str(lossHi))
      # os.system("chmod ugo+r "+ svgFile)
      os.system('python /Users/Annalise/GitHub/CompBioSummer2015/ReconConversion.py '+path2files+".newick"+" "+str(Dup)+" "+str(Trans)+" "+str(Loss)+" "+str(request.form['scoring'])+" "+str(switchLo)+" "+str(switchHi)+" "+str(lossLo)+" "+str(lossHi))
      with open(path2files+"freqFile.txt") as f:
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
      staticString = "<h4>Duplication Cost:"+str(Dup)+", Transfer Cost: "+str(Trans)+", Loss Cost: "+str(Loss)+"<br>Maximum Parsimony Cost: "+str(totalCost)+"<br>Your scoring method: "+scoreMethod+", Total Sum of Scores: "+str(totalFreq)+"<br>Total Number of Reconciliations: "+str(totalRecon)+"</h4>"
      for x in range(len(scoreList)):
        os.system("./vistrans -t "+path2files+".tree -s "+path2files+".stree -b "+path2files+str(x)+".mowgli.brecon -o "+path2files+str(x)+".svg")
        score = scoreList[x]
        percent = 100.0*score/totalFreq
        if x ==0:
          runningTot = percent
          carouselstr+='<li data-target="#results" data-slide-to="0" class="active"></li>'+"\n"
          carouselcap+="<div class='item active'><img src='/uploads/"+ Name+str(x)+".svg' alt='First slide' width='460' height='345'><div class='carousel-caption'><font color='black'><h3>Reconciliation 1 of "+str(len(scoreList))+"</h3><p>Score = "+str(score)+"<br>Percent of total = "+str(percent)+"%<br>Running total = "+str(runningTot)+"%</font></p></div></div>"+"\n"
          os.system("cp /Users/Annalise/GitHub/CompBioSummer2015/"+str(path2files)+str(x)+'.svg ' + UPLOAD_FOLDER)
        else:
          runningTotScore = runningTotal(scoreList, x)
          runningTot = 100.0*runningTotScore/totalFreq
          if runningTot > 100:
            runningTot = 100
          carouselstr+='<li data-target="#results" data-slide-to="'+str(x)+'"></li>'+"\n"
          carouselcap+="<div class='item'><img src='/uploads/"+ Name+str(x)+".svg' alt='First slide' width='460' height='345'><div class='carousel-caption'><font color='black'><h3>Reconciliation "+str(x+1)+" of "+str(len(scoreList))+"</h3><p>Score = "+str(score)+" <br>Percent of total = "+str(percent)+"%<br>Running total = "+str(runningTot)+"%</font></p></div></div>"+"\n"
          os.system("cp /Users/Annalise/GitHub/CompBioSummer2015/"+path2files+str(x)+'.svg ' + UPLOAD_FOLDER)
    staticString = Markup(staticString)
    carouselstr = Markup(carouselstr)
    carouselcap = Markup(carouselcap)
  return render_template("results.html", carouselstr = carouselstr, carouselcap = carouselcap, staticString = staticString)
def runningTotal(scoresList, index):
  runningTot = 0
  for n in range(len(scoresList)):
    if n<=index:
      runningTot += scoresList[n]
  return runningTot

def string2List(string):
  newList = []
  commaList = []
  for n in range(len(string)):
    if string[n:n+2]== ', ':
      commaList.append(n)
  if commaList == []:
    return [float(string[1:-3])]
  newList.append(float(string[1:commaList[0]]))
  for n in range(len(commaList)):
    if commaList[n] != commaList[-1]:
      newList.append(float(string[commaList[n]+2:commaList[n+1]]))
  newList.append(float(string[commaList[-1]+2:-2]))
  return newList

# @app.route('/show/<filename>')
# def uploaded_file(filename):
#   filename = 'http://127.0.0.1:5000/uploads/'+filename
#   return render_template('index.html', filename = filename)
# 

@app.route('/uploads/<filename>')
def send_file(filename):
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
if __name__ == "__main__":
  app.run()