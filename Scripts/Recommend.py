import numpy as np
import pandas as pd
import turicreate as tc

lib = tc.SFrame.read_csv('/Users/kf/Desktop/AppLibrary.csv')
plays = pd.read_csv('/Users/kf/Desktop/playlists.csv')

# Train or upload songs into recommender
m = tc.recommender.item_content_recommender.create(lib, "item_id")

# Get 10 most similar items for each item in each user's playlist
index=0
sf = tc.SFrame()
usersf = tc.SFrame()
playsf = tc.SFrame()
for i in plays['item_id']:
    cnt = 0
    while cnt < 10:
        temp = tc.SFrame(plays['user_id'].iloc[[index]])
        usersf = usersf.append(temp)
        #temp2 = tc.SFrame(plays['plays'].iloc[[index]])
        #playsf = playsf.append(temp2)
        cnt+=1
    index+=1
    sf = sf.append(m.get_similar_items([i],k=10))
    #print(m.get_similar_items([i]))

# Convert to dataframe and concatenate so we have recommendations
# for each song in each user's playlist
recommend = sf.to_dataframe()
user = usersf.to_dataframe()
#play = playsf.to_dataframe()

#final = pd.concat((user,play,recommend),axis=1)
final = pd.concat((user,recommend),axis=1)
#final.columns = ['user_id','plays','item_id','similar','score','rank']
final.columns = ['user_id','item_id','similar','score','rank']
uncoded = pd.read_csv('/Users/kf/Desktop/AppLibraryUC.csv',encoding='latin-1')
final = final.join(uncoded.set_index('songid'),on='item_id',how='left')
final = final.join(uncoded.set_index('songid'),on='similar',how='left',lsuffix='_item')
final.to_csv('/Users/kf/Desktop/final.csv') 

#Loop through the recommendations and drop any recommendations
#that the user already has in their playlist
newtoUser = pd.DataFrame()
for i in final['user_id'].unique():
    userdf = final.loc[final['user_id'] == i]
    listened = userdf['item_id'].unique()
    for x in userdf['similar']:
        if x in listened:
            droprows = userdf[userdf['similar'] == x].index
            userdf.drop(droprows, inplace=True)
    # ADD WEIGHTS IF THE ARTISTS ARE THE SAME, GENRE ARE THE SAME, ETC.
    for index, row in userdf.iterrows():
        if row["artist_item"]+row["album_item"] == row["artist"]+row["album"]:
            userdf["score"].loc[index] = userdf["score"].loc[index]*1.05
        elif row["artist_item"] == row["artist"]:
            userdf["score"].loc[index] = userdf["score"].loc[index]*1.04
        if row["genre_item"] == row["genre"]:
            userdf["score"].loc[index] = userdf["score"].loc[index]*1.02
    # Drop any songs that were recommended twice
    # (e.g. once for a david bowie song the user listened to and once for a beatles song)
    userdf = userdf.drop_duplicates(['similar'])
    # Sort values by score and then get the top 10 scores
    userdf = userdf.sort_values(by='score', ascending=False)
    userdf = userdf.nlargest(15, 'score')
    newtoUser = newtoUser.append(userdf)

newtoUser.to_csv('/Users/kf/Desktop/recommends.csv')

for u in newtoUser['user_id'].unique():
    print("***************************************")
    print("Welcome back!            User ID: ",u)
    print("-------------------")
    print("\nHere's what we recommend for you...")
    for index, row in newtoUser.iterrows():
        if u == row['user_id']:
            print("Because you listened to ",row['title_item']," by ",row['artist_item'],"\nWe recommend you check out ",row['title']," by ",row['artist'],"!\n")

#**********************************************************************
#GENERATE DATASET FOR VISUALS THAT SHOWS SIMILAR ITEMS FOR ALL SONGS
allsims = tc.SFrame()
for i in uncoded['songid']:
    allsims = allsims.append(m.get_similar_items([i],k=10))

allsimsDF = allsims.to_dataframe()
output = allsimsDF.join(uncoded.set_index('songid'),on='item_id',how='left')
output = output.join(uncoded.set_index('songid'),on='similar',how='left',lsuffix='_item')
output.to_csv('/Users/kf/Desktop/similarities.csv',index=False)

# Example of how we can measure model success
#print(m.evaluate_precision_recall(lib))
