import pandas as pd
import numpy as np
import json
import re

allsimilars = pd.read_csv("/Users/kf/Desktop/similarities.csv",encoding='latin-1')
similars = pd.read_csv("/Users/kf/Desktop/final.csv",encoding='latin-1',nrows=50)

#*******************************************
#*****MANIPULATE DATA FOR NETWORK GRAPH*****
#similars['songsource'] = similars['artist_item'] + ' - ' + similars['title_item']
#similars['songtarget'] = similars['artist'] + ' - ' + similars['title']

# Create a set of unique colours to assign to each song based on their genre.
# This makes it easier to colour to nodes in the network graph
colourbank = ["darkorange","tomato","maroon","slategray","mistyrose","indigo","royalblue","teal","papayawhip","gainsboro","lightsalmon","indianred","orange","peachpuff","darkkhaki","darkseagreen","olive","cadetblue","powderblue","dodgerblue","steelblue","thistle","mediumpurple","pink","seashell","linen","silver","wheat","peru","sienna","brown","black","cornsilk","crimson","coral","darkmagenta"]
x = allsimilars['genre'].unique()
x.sort()
colours = []
for idx, g in enumerate(x):
    colours.append(colourbank[idx])
colourkey = pd.DataFrame({'genre': x,'colour': colours})
colourkey.to_csv('/Users/kf/Desktop/colourkey.csv')

# Create links file with source as listened artists and
# targets as recommended artists. Also assign a colour to
# the artist based on their genre.
sources = []
sourcecolour = []
targets = []
targetcolour = []
for index, row in similars.iterrows():
    songS = row["artist_item"].encode("ascii", errors="ignore").decode()
    songT = row["artist"].encode("ascii", errors="ignore").decode()
    genreS = row["genre_item"].encode("ascii", errors="ignore").decode()
    genreT = row["genre"].encode("ascii", errors="ignore").decode()
    CS = colourkey[colourkey['genre']==genreS]['colour'].values
    CT = colourkey[colourkey['genre']==genreT]['colour'].values
    # Don't append when the listened artist is the same
    # as the recommended artists
    if songS == songT:
        pass
    else:
        sources.append(songS)
        sourcecolour.append(CS[0])
        targets.append(songT)
        targetcolour.append(CT[0])

links = pd.DataFrame(
    {'source': sources,
     'scolor': sourcecolour,
     'target': targets,
     'tcolor': targetcolour}
)

# Drop duplicates because two artists could be connected multiple times
# due to different songs matching up. We just want to see if they are
# connected, how many times or through what songs doesn't matter.
links = links.drop_duplicates(["source","target"])

links.to_csv('/Users/kf/Desktop/links.csv')

#*********************************************
#*****MANIUPULATE DATA FOR TREEMAP VISUAL*****
# Get how many times each artist was recommended
simItems = np.array(allsimilars['artist'])
unique, counts = np.unique(simItems, return_counts=True)
#print(np.asarray((unique, counts)).T)

# Get how many songs the artist has in the library
songs = allsimilars.drop_duplicates(["item_id"])
artistCount = np.array(songs['artist_item'])
uniqueA, countsA = np.unique(artistCount, return_counts=True)
#print(np.asarray((uniqueA, countsA)).T)

for i in uniqueA:
    if i not in unique:
        print(i)

# Put results in dataframe
treedata = pd.DataFrame(
    {'artist': unique,
     'recommends': counts,
     'songs': countsA}
)

# Get the genres each artist belongs to and combine it with the treedata
genres=[]
for i in treedata['artist']:
    index = max(allsimilars[allsimilars['artist'] == i].index)
    genre = str(allsimilars['genre'].iloc[[index]].values)
    genre = genre.replace("['","")
    genre = genre.replace("']","")
    genres.append(genre)

genresPD = pd.DataFrame(
    {'genre': genres}
)

treedata = pd.concat((treedata,genresPD),axis=1)
treedata['rps'] = treedata['recommends']/treedata['songs']
treedata['rps'] = treedata['rps'].round(2)
treedata.to_csv('/Users/kf/Desktop/treemap.csv')
    
