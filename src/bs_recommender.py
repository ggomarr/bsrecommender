import os
import json
import requests
import pandas as pd
from flask import Flask,request,jsonify
from flask_cors import CORS

songs_file='./data/songs.txt'
with open(songs_file,'r') as f:
    songs={song.strip().split(',',1)[0]:json.loads(song.strip().split(',',1)[1]) for song in f.readlines()}
    
likeness_file='./data/likeness.txt'
likeness=pd.read_csv(likeness_file,index_col=[0,1],names=['counts'])

songs_bookmarked_by='https://bsaber.com/wp-json/bsaber-api/songs/?bookmarked_by={usr}&count={cnt}&page={pag}'
drop_song_keys=['song_key','hash']
new_bookmarks_file='./data/new_bookmarks.txt'

def find_user_bookmarks(user):
    bookmarks={}
    pag=1
    while pag:
        url=songs_bookmarked_by.format(usr=user,cnt=200,pag=pag)
        try:
            chunk=requests.get(url).json()
            bookmarks.update({song['song_key']:{key:song[key] for key in song if key not in drop_song_keys} \
                              for song in chunk['songs']})
            pag=chunk['next_page']
        except:
            pag=None
    if len(bookmarks)>0:
        with open(new_bookmarks_file,'a+') as f:
            f.write('{},{}\n'.format(user,json.dumps(bookmarks)))
    return list(bookmarks.keys())
    
def find_similar_items(item,likeness):
    matches=[]
    try:
        matches=matches+[ likeness.xs(item,level=0) ]
    except:
        pass
    try:
        matches=matches+[ likeness.xs(item,level=1) ]
    except:
        pass
    if len(matches)>0:      
        return pd.concat(matches).rename_axis('song').reset_index()
    else:
        return pd.DataFrame(columns=['song','counts'])

def give_me_recs(songs_lst,likeness,num=50):
    recs=pd.concat([find_similar_items(song,likeness) for song in songs_lst]).groupby('song')['counts'].sum()
    recs=recs.loc[~recs.index.isin(songs_lst)].sort_values(ascending=False).head(num).reset_index()
    recs['title']=recs['song'].apply(lambda x: songs[x]['title'])
    recs['curator']=recs['song'].apply(lambda x: songs[x]['curated_by'] if 'curated_by' in songs[x] else '')
    return recs.set_index('song').to_dict(orient='index')
    
app=Flask(__name__)
app.config['JSON_SORT_KEYS']=False
CORS(app) 
        
@app.route('/', methods=['GET'])
def recommend_songs():
    liked=['']
    try:
        liked=liked+find_user_bookmarks(request.args.get('user'))
    except:
        pass
    try:
        liked=liked+request.args.get('liked').split(',')
    except:
        pass
    return jsonify(give_me_recs(liked,likeness,25))

if __name__=='__main__':
    if 'BSREC_DEBUG' in os.environ and os.environ['BSREC_DEBUG']=='1':
        debug=True
    else:
        debug=False
    app.run(host='0.0.0.0',port=5000,debug=debug)
