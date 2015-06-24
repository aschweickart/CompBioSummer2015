#!/usr/local/bin/python

import os
import time
import sys
from flask import Flask, request, redirect, url_for, render_template, session
from werkzeug import secure_filename
from flask_recaptcha import ReCaptcha
import xscape.costscape2
import xscape.sigscape2
import xscape.eventscape2
import xscape.tree2newick
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/Users/Annalise/Desktop/UploadFolder/'



ALLOWED_EXTENSIONS = set(['newick', 'tree'])
recaptcha = ReCaptcha(app, '6LecfwcTAAAAAFzGRnCkI0TuCeJJwgCf2rlYqAcG', '6LecfwcTAAAAAMNXwglJ0UEJORZPIiPU2nnk6cGR')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/Registration')
def registration():
    return render_template('form.html')

def fileName():
        email = request.form['email']
        for i in range(len(email)):
                if email[i] == '@':
                        return email[0:i]

@app.route('/store_user', methods=['GET', 'POST'])
def store_user(message = None):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        institution = request.form['inst']
        entry = ";".join([name, institution, email])
        file = open('registered.txt', 'a')
        file.write(entry +'\n')
        file.close()
        file1 = fileName()
        os.system("mkdir "+file1)
        app.config['UPLOAD_FOLDER'] = '/Users/Annalise/Desktop/UploadFolder/'+file1
        os.system('cp -R xscape '+ file1)
        os.system("mkdir results")
        os.system("mv results "+ file1)
    return render_template('signup.html', message = 'Now Log in with your new account!')

def registered():
    email = request.form['email']
    searchfile = open('registered.txt', 'r')
    match = False
    for line in searchfile:
        if email in line:
            match = True
        else:
            if match == True:
                match = True
            else: match = False
    return match

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if recaptcha.verify() and registered():
            return render_template('upload.html')
        else:
            pass
    return render_template('signup.html', message = 'There was something wrong with your login. Please try again.')

@app.route('/signup')
def signup(message = None):
    return render_template('signup.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def outputFile(fileName):
    if fileName[-6:] == "newick":
        return fileName[:-7]
    elif filename[-4:] =="tree":
        return fileName[:-5]

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file(message = None):
    if request.method == 'POST':
        file = request.files['trees']
        app.config['UPLOAD_FOLDER'] = '/Users/Annalise/Desktop/UploadFolder/' + fileName() + '/xscape/'
        if file and allowed_file(file.filename):
            if file.filename[-4:] == "tree":
                treeFile = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], treeFile))
                os.system("python "+ fileName() +"/xscape/tree2newick.py " + fileName() +"/xscape/"+treeFile+ " "+treeFile[:-5]+".newick")
                filename = treeFile[:-5] + ".newick"
            else:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            list1 = request.form.getlist('tool')
        #View_Tanglegram
        if 'view_tanglegram' in list1:
            path2tanglegram = fileName() + '/xscape/view_tanglegram'
            path2newick = fileName() + '/xscape/'+ filename
            os.system('python ' +path2tanglegram + " -n -g "+outputFile(filename) +".svg "+ path2newick)
            path2svg = fileName() + '/results'
            if os.path.exists(outputFile(filename) +".svg"):
                os.system("mv "+ outputFile(filename)+".svg " + path2svg)
            else: return render_template('upload.html', message = 'There was something wrong with your file. Please see documentation.') 
        #Costscape
        if 'costscape' in list1:
            if request.form['csswitchlow']!= '':
                switchLo = request.form['csswitchlow']
            else: switchLo = 0.1
            if request.form['csswitchhigh'] != '':
                switchHi = request.form['csswitchhigh']
            else: switchHi = 5
            if request.form['cslosslow'] != '':
                lossLo = request.form['cslosslow']
            else: lossLo = 0.1
            if request.form['cslosshigh'] != '':
                lossHi = request.form['cslosshigh']
            else: lossHi = 5
            if request.form['cslog'] == 'yes':
                log = True
            else: log = False
            path2costscape = fileName() + '/xscape/costscape2.py '
            path2newick = fileName() + '/xscape/' + filename
            os.system('python ' + path2costscape + path2newick + " " + str(switchLo) + " " + str(switchHi) + " " + str(lossLo) + " "+ str(lossHi) + " "+ str(log))
            path2pdf = fileName() + '/xscape/' + outputFile(filename) + "costscape.pdf"
            if os.path.exists(path2pdf):
                os.system("mv " + path2pdf+ " " + fileName() + "/results")
                path2txt = fileName() + '/xscape/' + outputFile(filename) + "costscape.txt"
                os.system("mv " +path2txt+" " + fileName() + "/results")       
            else:
                return render_template('upload.html', message = 'There was something wrong with your file. Please see documentation.')       
        #Sigscape
        if 'sigscape' in list1:
            if request.form['ssswitchlow']!= '':
                switchLo = request.form['ssswitchlow']
            else: switchLo = 0.1
            if request.form['ssswitchhigh'] != '':
                switchHi = request.form['ssswitchhigh']
            else: switchHi = 5
            if request.form['sslosslow'] != '':
                lossLo = request.form['sslosslow']
            else: lossLo = 0.1
            if request.form['sslosshigh'] != '':
                lossHi = request.form['sslosshigh']
            else: lossHi = 5
            if request.form['randomization'] != '':
                randomization = request.form['randomization']
            else: randomization = 100
            if request.form['sslog'] == 'yes':
                log = True
            else: log = False
            path2sigscape = fileName() + '/xscape/sigscape2.py '
            path2newick = fileName() + '/xscape/' + filename
            os.system('python ' + path2sigscape + path2newick + " " + str(switchLo) + " " + str(switchHi) + " " + str(lossLo) + " "+ str(lossHi) + " "+ str(log) +" "+str(randomization))
            path2pdf = fileName() + '/xscape/' + outputFile(filename) + "sigscape.pdf"
            if os.path.exists(path2pdf):
                os.system("mv " + path2pdf+ " " + fileName() + "/results")
                path2txt = fileName() + '/xscape/' + outputFile(filename) + "sigscape.txt"
                os.system("mv " +path2txt+" " + fileName() + "/results")         
            else:
                return render_template('upload.html', message = 'There was something wrong with your file. Please see documentation.')
        #Eventscape
            if request.form['esswitchlow']!= '':
                switchLo = request.form['esswitchlow']
            else: switchLo = 0.1
            if request.form['esswitchhigh'] != '':
                switchHi = request.form['esswitchhigh']
            else: switchHi = 5
            if request.form['eslosslow'] != '':
                lossLo = request.form['eslosslow']
            else: lossLo = 0.1
            if request.form['eslosshigh'] != '':
                lossHi = request.form['eslosshigh']
            else: lossHi = 5
            UorI = request.form['UorI']
            path2eventscape = fileName() + '/xscape/eventscape2.py'
            path2newick = fileName() + '/xscape/' + filename
            os.system('python '+ path2eventscape +" "+ path2newick +" "+ str(switchLo) + " "+ str(switchHi)+" "+ str(lossLo)+" "+str(lossHi)+" "+ str(UorI))
            path2csv = fileName() + '/xscape/' + outputFile(filename) + ".csv"
            if os.path.exists(path2csv):
                os.system("mv " + path2csv+ " " + fileName() + "/results")
            else:
                return render_template('upload.html', message = 'There was something wrong with your file. Please see documentation.')
        if os.listdir(fileName() + '/results/') != []:
            os.system("tar -zcvf results.tar.gz "+fileName()+"/results/")
            os.system("mv results.tar.gz "+fileName())
        list2 = request.form.getlist('deletion')
        if 'deleteFile' in list2:
            os.system('rm '+ fileName()+'/xscape/'+filename)
            if os.path.exists(fileName()+'/xscape/'+treeFile):
                os.system('rm '+fileName()+'/xscape/'+treeFile)
        #SEND_MAIL HERE!!
        # if 'deleteResults' in list2:
        #     os.system('rm ' + fileName()+'/results.tar.gz')
        #     os.system('rm '+fileName() + '/results/*')
    return render_template('upload.html', message='Your files have been sent to your email!')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        institution = request.form['inst']
        entry = ';'.join([str(time.time()), name, email, institution])
        file = open('downloads.txt', 'a')
        file.write(entry + '\n')
        file.close()
    return render_template('download.html')

def send_mail(send_from, send_to, subject, text, files=[],
              server="smtp.cs.hmc.edu"):
    assert type(send_to)==list
    assert type(files) == list
    SUBJECT = subject
    msg = MIMEMultipart()
    msg['From']=send_from,
    msg['To']=', '.join(send_to),
    msg['Date']=formatdate(localtime=True),
    msg['Subject']= SUBJECT
    
    msg.attach(MIMEText(text))

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(file, "rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content=Disposition', 'attachment; filename="%s"' %os.path.basename(f))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


if __name__ == "__main__":
        app.run()