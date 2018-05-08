#!flask/bin/python
from flask import Flask, render_template, request, url_for
import werkzeug
import os
from celery import Celery
import requests
import spotipy
import spotipy.oauth2 as oauth2
import pandas as pd
import numpy as np
import sklearn
from sklearn.ensemble import RandomForestClassifier
import time

app = Flask(__name__)
app.secret_key = "sitedigoloquediego"


application = app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
##extract song meta
def searchit(song):
    credentials = oauth2.SpotifyClientCredentials(
        client_id="ID",
        client_secret= "SECRET")

    token = credentials.get_access_token()
    
    headers = {'Accept': 'application/json','Content-Type': 'application/json','Authorization': 'Bearer '+ token}

    params = {'q': song, 'type': 'track', 'market': 'es', 'limit': '1'}
    response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)

    results=response.json()
    r=results['tracks']['items']

    ids = r[0]['id']
    name = r[0]['name']
    artist= r[0]['artists'][0]['name']
    pop = r[0]['popularity']

    features = requests.get('https://api.spotify.com/v1/audio-features/'+ids, headers=headers)

    results=features.json()


    loudness= results['loudness']
    danceability=results['danceability']
    valence=results['valence']
    tempo= results['tempo']
    energy=results['energy']
    liveness=results['liveness']
    key=results['key']
    acoustic=results['acousticness']
    speech=results['speechiness']


    df = pd.DataFrame({'loud': [loudness], 'dance': [danceability],'valence': [valence],'tempo': [tempo],'energy': [energy],'live': [liveness],'key': [key],'acoustic': [acoustic],'speech': [speech]})

    df.to_csv('test2.csv', sep=',', encoding='utf-8',header=True, index=False, columns=['loud', 'dance', 'valence', 'tempo','energy','live','key','acoustic','speech'])
    
    return (name, artist, pop)


@app.route('/')
def index():
    
    return render_template('index.html')


@app.route('/', methods=['POST'])
def processspotify():


    song = request.form['song']
    print (song)
    name=searchit(song)[0]
    artist=searchit(song)[1]
    pop=searchit(song)[2]
    print (name)
    return render_template('results.html', name=name, artist=artist, pop=pop)

#@app.errorhandler(Exception)
#def all_exception_handler(error):
#    return '<p>A PROBLEM, DUDE!</p>', 500

@app.route('/estimation/', methods=['POST'])
def predictsong():
    df = pd.read_csv("musicot1.csv", sep=',')
    X_df = df.iloc[:,:-1]
    X = X_df.as_matrix()
    y_df = df["type"].values
# sklearn can only deal with numpy arrys
    y = np.array([1 if i>=1 else 0 for i in y_df])
    
    probs=[]
    for i in range(1,80):
        clf = RandomForestClassifier(n_estimators = 19, max_features=None,max_depth =None)
        clf.fit(X,y)
        test= pd.read_csv("test2.csv", sep=',')
        T= test.as_matrix()
        pred= clf.predict(T)
        prob= clf.predict_proba(T)
        probs.append([prob[:,1]])
        
    mean= np.mean(probs)  
    probability="{:.0%}".format(mean)
    probability=probability[:-1]
    message1="Éxito casi seguro"
    message2= "No es madera de éxito del verano"
    final= message1 if mean > np.array([0.329]) else message2
    print(probs)
    return render_template('results.html',probability=probability, message=final)
if __name__ == '__main__':
    app.run(debug=True)

