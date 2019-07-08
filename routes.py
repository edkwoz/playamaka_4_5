from flask import Flask, render_template, request, session
from forms import SupaPlayaMaka
import requests, json, os
from ftplib import FTP


app = Flask(__name__)
app.secret_key = "TEST"


@app.route('/', methods=['GET', 'POST'] )
def index():
    return render_template('index.html')



###########
#controller gets the number of files you want to enter, before going to type in the file names
@app.route('/howmany', methods=['GET', 'POST'] )
def howmany():
    form = SupaPlayaMaka()
    return render_template('howmany.html', form=form)



###########
#controller gets the number of files you want to enter, before going to type in the file names
@app.route('/howmany_AD', methods=['GET', 'POST'] )
def howmany_AD():
    form = SupaPlayaMaka()
    return render_template('howmany_AD.html', form=form)



###########
#controller makes text inputs based on the number entered in howmany
@app.route('/enterfiles', methods=['GET', 'POST'] )
def enterfiles():
    form = SupaPlayaMaka()
    numfiles = request.form.get('amount')
    numfilesint = int(numfiles)
    session['x'] = 1
    return render_template('enterfiles.html',form=form, numfilesint=numfilesint)


###########
#controller makes text inputs based on the number entered in howmany
@app.route('/enterfiles_AD', methods=['GET', 'POST'] )
def enterfiles_AD():
    form = SupaPlayaMaka()
    numfiles = request.form.get('amount')
    numfilesint = int(numfiles)
    session['x'] = 1
    return render_template('enterfiles_AD.html',form=form, numfilesint=numfilesint)



###########
#controller allows files to be input for video names to playeropts
@app.route('/selectfiles', methods=['GET', 'POST'] )
def selectfiles():
    form = SupaPlayaMaka()
    playa_option = request.form['playerchoice']
    session['player_option'] = playa_option
    session['x'] = 0
    return render_template('selectfiles.html', form=form)



###########
#controller makes form for selecting player type
@app.route('/playeropts1', methods=['GET', 'POST'] )
def playeropts1():
    form = SupaPlayaMaka()
    return render_template('playeropts1.html', form=form)



###########
#controller takes file names from selectfiles or enterfiles and goes to entry ids
@app.route('/entryids', methods=['GET', 'POST'] )
def entryids():
    form = SupaPlayaMaka()
    x = session.get('x', None)
    if x == 0:
        files = request.form.getlist('videofile')
        newfiles = []
        for f in files:
            newf = os.path.splitext(f)[0]
            newfiles.append(newf)
        session['file_var'] = newfiles
        return render_template('entryids.html', form=form, newfiles=newfiles)
    else:
        files = request.form.getlist('filename')
        newfiles = []
        for f in files:
            newfiles.append(f)
        session['file_var'] = newfiles
        return render_template('entryids.html', form=form, newfiles=newfiles)




###########
#controller takes file names from selectfiles or enterfiles and goes to entry ids
@app.route('/entryids_AD', methods=['GET', 'POST'] )
def entryids_AD():
    form = SupaPlayaMaka()
    x = session.get('x', None)
    if x == 0:
        files = request.form.getlist('videofile')
        newfiles = []
        for f in files:
            newf = os.path.splitext(f)[0]
            newfiles.append(newf)
        session['file_var'] = newfiles
        return render_template('entryids_AD.html', form=form, newfiles=newfiles)
    else:
        files = request.form.getlist('filename')
        newfiles = []
        for f in files:
            newfiles.append(f)
        session['file_var'] = newfiles
        return render_template('entryids_AD.html', form=form, newfiles=newfiles)



###########
#controller takes file names, entry ids, and player option and outputs code
@app.route('/codeout', methods=['GET', 'POST'] )
def codeout():
    download_option = request.form['downloadopts']
    # session['download_option'] = download_option
    # session['x'] = 0
    player_option = session.get('player_option', None)
    files = session.get('file_var', None)
    length = len(files)
    entryids = request.form.getlist('entryid')
    if player_option == 'standardplayer':
        return render_template('standardplayer.html', files=files, entryids=entryids, length=length, download_option=download_option)
    elif player_option == 'audioplayer':
        return render_template('audioplayer.html', files=files, entryids=entryids, length=length, download_option=download_option)
    else:
        return render_template('chapterplayer.html', files=files, entryids=entryids, length=length, download_option=download_option)



def selectfiles():
    form = SupaPlayaMaka()
    download_option = request.form['downloadopts']
    session['download_option'] = download_option
    session['x'] = 0
    return render_template('selectfiles.html', form=form)


###########
#controller takes file names, entry ids, and player option and outputs code
@app.route('/codeout_AD', methods=['GET', 'POST'] )
def codeout_AD():
    files = session.get('file_var', None)
    length = len(files)
    entryids = request.form.getlist('entryid')
    file_idlist = []
    for f in files:
        caption_filename = f
        url_g = 'http://api.3playmedia.com/files?apikey=qPkBhpMQzvvZFJqbAw5MgaWwVMmUZtRX&q=name=%s' % caption_filename
        g = requests.get(url_g)
        response = g.text
        listofdicts = json.loads(response)
        dictchoice = listofdicts['files']
        finaldict = dictchoice[0]

        for key, value in finaldict.items():
            if key == 'id':
                file_id = value
                break
            else:
                continue

        file_idlist.append(file_id)
    return render_template('audio_description.html', files=files, entryids=entryids, length=length, file_idlist=file_idlist, listofdicts=listofdicts, dictchoice=dictchoice, finaldict=finaldict)



###########
#controllers fill video id field in 3play for captions
@app.route('/captions1', methods=['GET', 'POST'] )
def captions1():
    form = SupaPlayaMaka()
    if request.method == 'POST':
        return redirect(url_for('captions2'))
    elif request.method == 'GET':
        return render_template('captions1.html', form=form)

@app.route('/captions2', methods=['GET', 'POST'] )
def captions2():
    form = SupaPlayaMaka()
    # gets files from form
    files = request.form.getlist('captionfile')
    # strips the file extension from the file input and makes new list
    newfiles = []
    for f in files:
        newf = os.path.splitext(f)[0]
        newfiles.append(newf)

    # issues get request to 3play api to get the id# of the named file
    file_idlist = []
    for f in newfiles:
        caption_filename = f
        url_g = 'http://api.3playmedia.com/files?apikey=qPkBhpMQzvvZFJqbAw5MgaWwVMmUZtRX&q=name=%s' % caption_filename
        g = requests.get(url_g)
        response = g.text
        listofdicts = json.loads(response)
        dictchoice = listofdicts['files']
        finaldict = dictchoice[0]

        for key, value in finaldict.items():
            if key == 'id':
                file_id = value
                break
            else:
                continue

        file_idlist.append(file_id)

    # issues the put request, using the id# to populate the video id
    i = 0
    for f in newfiles:
        caption_filename = f
        file_id = file_idlist[i]
        url_p = 'http://api.3playmedia.com/files/%s' % file_id
        params_p = {'apikey':'qPkBhpMQzvvZFJqbAw5MgaWwVMmUZtRX', 'api_secret_key':'dMkGa_CVlIjL8clh3I3bPfH0EQrgp_w7', '_method':'PUT', 'video_id':'%s' % caption_filename}
        p = requests.put(url_p, params=params_p)
        i += 1

    return render_template('captions2.html', newfiles=newfiles)





if __name__ == "__main__":
  app.run(debug=False)
