import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn import preprocessing
import random
pd.set_option('display.max_columns', 500)

# ***** CLEAN AND ASSESS DATA *****
songs = pd.read_csv("/Users/kf/Desktop/Master.csv",encoding = "ISO-8859-1")
users = pd.read_csv("/Users/kf/Desktop/Users.csv",nrows=10)
#print("\nCount of Null Values per Column:\n",songs.isnull().sum())

#Find null values in a column
#songs[songs["genre"].isnull()]
#print(songs["year"].unique())
#print(songs["genre"].unique())
#uniqueartists = songs["artist"].unique()
#uniqueartists.sort()
#print(uniqueartists)

songs['genre'].loc[songs['genre'].str.contains('Indie', na = False)] = 'Indie Rock'
songs['genre'].loc[songs['genre'].str.contains('Hip', na = False)] = 'Hip-Hop'
songs['genre'].loc[songs['genre'].str.contains('Rap', na = False)] = 'Hip-Hop'
songs['genre'].loc[songs['genre'].str.contains('Post-rock', na = False)] = 'Post-Rock'
songs['genre'].loc[songs['genre'].str.contains('Pop', na = False)] = 'Pop'
songs['genre'].loc[songs['genre'].str.contains('Alt', na = False)] = 'Alternative Rock'
songs['genre'].loc[songs['genre'].str.contains('Punk', na = False)] = 'Punk'
songs['genre'].loc[songs['genre'].str.contains('Funk', na = False)] = 'Funk'
songs['genre'].loc[songs['genre'].str.contains('Jazz', na = False)] = 'Jazz'
songs['genre'].loc[songs['genre'].str.contains('Experiment', na = False)] = 'Experimental'
songs['genre'].loc[songs['genre'].str.contains('Synth', na = False)] = 'Synthpop'

#Replace values in a column based on two conditions
#songs["genre"][(songs["artist"] == "Gorillaz") & (songs["genre"] == "Unknown genre")] = "Pop"

# ***** TRANSFORM DATA *****
nums = songs.select_dtypes(exclude=object)
objs = songs.select_dtypes(include=object)

print(nums.describe())
print(objs.describe())

# Graph the histogram distributions for each numerical variable
for i in list(nums.columns):
    if i != "songid":
        songs[i].hist(bins=10)
        title = i + " Distribution/Histogram"
        plt.title(title)
        plt.show()
# Graph the histogram distributions for each categorical variable
for i in list(objs.columns):
    if i == "genre":
        sn.barplot(objs[i].value_counts().values, objs[i].value_counts().index, alpha=0.8)
        title = i + " - Data Distribution"
        plt.title(title)
        plt.show()

# Drop sample rate and bit rate as both are not very informative
nums = nums.drop(columns=['sampleRate', 'bitRate', 'audioOffset'])

# Categorize duration column
duration=[]
for i in nums["duration"]:
    if i < 120:
        duration.append("0- Short")
    elif i >= 120 and i < 240:
        duration.append("1 - Medium")
    elif i >= 240 and i < 360:
        duration.append("2 - Long")
    elif i >= 360:
        duration.append("3 - Very Long")

# Categorize duration column
decades=[]
for i in nums["year"]:
    if i < 1950:
        decades.append("Classic Era")
    elif i >= 1950 and i <= 1959:
        decades.append("1950s")
    elif i >= 1960 and i <= 1969:
        decades.append("1960s")
    elif i >= 1970 and i <= 1979:
        decades.append("1970s")
    elif i >= 1980 and i <= 1989:
        decades.append("1980s")
    elif i >= 1990 and i <= 1999:
        decades.append("1990s")
    elif i >= 2000 and i <= 2009:
        decades.append("2000s")
    elif i >= 2010 and i <= 2019:
        decades.append("2010s")
    elif i >= 2020 and i <= 2029:
        decades.append("2020s")

# Categorize tempo column based on metronome tempos
# http://www2.siba.fi/muste1/index.php?id=102&la=en
tempo=[]
for i in nums["tempo"]:
    if i < 50:
        tempo.append("0 - Grave")
    elif i >= 50 and i < 60:
        tempo.append("1 - Lento")
    elif i >= 60 and i < 72:
        tempo.append("2 - Adagio")
    elif i >= 72 and i < 84:
        tempo.append("3 - Maestoso")
    elif i >= 84 and i < 100:
        tempo.append("4 - Andante")
    elif i >= 100 and i < 120:
        tempo.append("5 - Moderato")
    elif i >= 120 and i < 144:
        tempo.append("6 - Allegro")
    elif i >= 144 and i < 160:
        tempo.append("7 - Vivace")
    elif i >= 160 and i < 200:
        tempo.append("8 - Presto")
    elif i >= 200:
        tempo.append("9 - Prestissimo")

# Categorize tuning column
# Librosa tuning reference is A440 standard pitch
tuning=[]
for i in nums["tuning"]:
    if i < -0.4:
        tuning.append("0 - Flat5")
    elif i >= -0.4 and i < -0.3:
        tuning.append("1 - Flat4")
    elif i >= -0.3 and i < -0.2:
        tuning.append("2 - Flat3")
    elif i >= -0.2 and i < -0.1:
        tuning.append("3 - Flat2")
    elif i >= -0.1 and i < 0:
        tuning.append("4 - Flat1")
    elif i == 0:
        tuning.append("5 - A440")
    elif i > 0 and i <= 0.1:
        tuning.append("6 - Sharp1")
    elif i > 0.1 and i <= 0.2:
        tuning.append("7 - Sharp2")
    elif i > 0.2 and i <= 0.3:
        tuning.append("8 - Sharp3")
    elif i > 0.3 and i <= 0.4:
        tuning.append("9 - Sharp4")
    elif i > 0.4:
        tuning.append("10 - Sharp5")
    
nums = nums.drop(columns=['duration','tempo','tuning','year'])
new = pd.DataFrame(
    {'duration': duration,
     'tempo': tempo,
     'tuning': tuning,
     'year': decades
    }
)

objs = pd.concat([objs,new],axis=1)
#Make a copy to reference during output
songsUncoded = pd.concat([objs,nums],axis=1)
songsUncoded.to_csv('/Users/kf/Desktop/AppLibraryUC.csv',index=False)

# Encode categorical variables into numerics
# - datamap variable is used to track what category corresponds to what number in each column
datamap={}
le = preprocessing.LabelEncoder()
objs = objs.drop(columns=["title"])
for i in list(objs.columns):
    labels = objs[i]
    lefit = le.fit(labels)
    objs[i] = lefit.transform(objs[i])
    le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
    datamap[i]=le_name_mapping

songsT = pd.concat([objs,nums],axis=1)
songsT.rename(columns={'songid':'item_id'}, inplace=True)
songsT.to_csv('/Users/kf/Desktop/AppLibrary.csv',index=False)

# Create a copy of dataframe that we can iterate over and extract data from
temp = songsT.copy()
# Create user_id column and insert value to represent the library
temp['user_id'] = '1'
# Create dataframe to host random song items for each user
playlists=pd.DataFrame()

upperlim = len(songsT)-1
# Iterate through each user
for i in users['user']:
    # Create a list of 5 random integers between within the limits of the library
    randints = random.sample(range(upperlim), 5)
    # Create playlist - Use each integer in the list to get the song
    # id and attach it to the current user
    for x in randints:
        # Change value x row's value in user_id column to the current user's id
        temp.set_value(x, 'user_id', i)
        # Store x row in a variable
        val = temp.iloc[[x]]
        # Reset index so we an concat dataframes properly
        val = val.reset_index(drop=True)
        # Create a dataframe with one value - a random number of plays
        rand = pd.DataFrame([random.randint(1,15)],columns=['plays'])
        # Concatenate plays with current song
        entry = pd.concat((val,rand),axis=1)
        # Add it to the users playlist
        playlists = playlists.append(entry)

playlists = playlists.reset_index(drop=True)
playlists = playlists.drop(columns=['plays'])
playlists.to_csv('/Users/kf/Desktop/playlists.csv',index=False)
        
