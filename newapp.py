from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename
import MasterReconciliation
import os


app = Flask(__name__)
UPLOAD_FOLDER = '/Users/Annalise/GitHub/CompBioSummer2015/svgFiles'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/index')
def index():
	return render_template('index.html')


@app.route('/form')
def form():
	return render_template('form.html')


@app.route('/reconcile', methods = ['GET', 'POST'])
def reconcile(carousel = None):
  if request.method == 'POST':
    file = request.files['newick']
    Dup = request.form['dup']
    Trans = request.form['trans']
    Loss = request.form["loss"]
    K = request.form['k']
    if file:
      filename = secure_filename(file.filename)
      Name = filename[:-7]
      os.system("mkdir "+Name)
      path2files = Name + '/' + Name
      svgFile = Name + "0.svg"
      file.save('/Users/Annalise/GitHub/CompBioSummer2015/'+path2files + ".newick")
      os.system("python /Users/Annalise/GitHub/CompBioSummer2015/MasterReconciliation.py "+path2files+".newick"+" "+Dup+" "+Trans+" "+Loss+" "+K)
      # os.system("chmod ugo+r "+ svgFile)
      htmlString1 = ""
      htmlString2 = ""
      for x in range(int(K)):
        os.system("./vistrans -t "+path2files+".tree -s "+path2files+".stree -b "+path2files+str(x)+".mowgli.brecon -o "+path2files+str(x)+".svg")
        if x ==0:
          htmlString1+='<li data-target="#results" data-slide-to="0" class="active"></li>'
          htmlString2+="<div class='item active'><img src='http://127.0.0.1:5000/uploads/"+ Name+str(x)+".svg' alt='First slide' width='460' height='345'></div>"
          os.system("cp /Users/Annalise/GitHub/CompBioSummer2015/"+path2files+str(x)+'.svg ' + UPLOAD_FOLDER)
        else:
          htmlString1+='<li data-target="#results" data-slide-to="'+str(x)+'"></li>'
          htmlString2+="<div class='item'><img src='http://127.0.0.1:5000/uploads/"+ Name+str(x)+".svg' alt='First slide' width='460' height='345'></div>"
          os.system("cp /Users/Annalise/GitHub/CompBioSummer2015/"+path2files+str(x)+'.svg ' + UPLOAD_FOLDER)
  return '''<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">

<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>K-best</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
      <style>
  .carousel-inner > .item > img,
  .carousel-inner > .item > a > img {
      width: 70%;
      margin: auto;
  }
  </style>
</head>
<body>
<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
      <div class="page-header">
        <h1>Results</h1>
      </div>
      <div class="container">
      <br>
      <div id="results" class="carousel slide" data-ride="carousel">
        <ol class="carousel-indicators">
          '''+htmlString1+'''
        </ol>
        <div class="carousel-inner" role="listbox">
          '''+htmlString2+'''
        </div>
        <a class="left carousel-control" href="#results" role="button" data-slide="prev">
          <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
          <span class="sr-only">Previous</span>
        </a>
        <a class="right carousel-control" href="#results" role="button" data-slide="next">
          <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
          <span class="sr-only">Next</span>
        </a>
      </div>
      </div>
       <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="../../dist/js/bootstrap.min.js"></script>
    <script src="../../assets/js/docs.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../../assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>'''

# @app.route('/show/<filename>')
# def uploaded_file(filename):
#       filename = 'http://127.0.0.1:5000/uploads/'+filename
#       return render_template('index.html', filename = filename)
# 

@app.route('/uploads/<filename>')
def send_file(filename):
        return send_from_directory(UPLOAD_FOLDER, filename )

# @app.route('/show/<filename>')
# def uploaded_file(filename):
# 	filename = 'http://127.0.0.1:5000/uploads/'+filename
# 	return render_template('index.html', filename = filename)
#   filename = 'http://127.0.0.1:5000/uploads/'+filename
#   return render_template('index.html', filename = filename)
# 

@app.route('/uploads/<filename>')
def send_file(filename):
	return send_from_directory(UPLOAD_FOLDER, filename )

if __name__ == "__main__":
	app.run() 
