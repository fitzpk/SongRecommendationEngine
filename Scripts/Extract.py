import os
import numpy as np
import pandas as pd
import librosa
from tinytag import TinyTag

directory_in_str = '/Users/kf/Desktop/songlibrary/'
directory = os.fsencode(directory_in_str)
artist = []
title = []
album = []
duration = []
year = []
genre = []
audio_offset = []
bitrate = []
samplerate = []
tempos = []
tunings = []
zeroCrossing = []
specCentroid = []
specBandwidth = []
specRolloff = []
chroma = []

counter = 0
#Loop through each mp3 in the folder/directory
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".mp3") or filename.endswith(".MP3"):
        try:
            #Concatenate directory_in_str and filename, then plug into TinyTag
            songpath = directory_in_str + filename
            tag = TinyTag.get(songpath)

            #Extract each songs metadata
            artist.append(tag.artist)
            title.append(tag.title)
            album.append(tag.album)
            duration.append(tag.duration)
            year.append(tag.year)
            genre.append(tag.genre)
            audio_offset.append(tag.audio_offset)
            bitrate.append(tag.bitrate)
            samplerate.append(tag.samplerate)

            #Extract each songs audio metrics
            y, sr = librosa.load(songpath)
            y_harmonic, y_percussive = librosa.effects.hpss(y)
            tempo, beats = librosa.beat.beat_track(y=y_percussive, sr=sr)
            tuning = librosa.estimate_tuning(y=y_harmonic, sr=sr)
            zcr = librosa.feature.zero_crossing_rate(y)
            spectral_centroids = librosa.feature.spectral_centroid(y, sr=sr)
            spec_bw = librosa.feature.spectral_bandwidth(y, sr=sr)
            rolloff = librosa.feature.spectral_rolloff(y, sr=sr)
            chroma_stft = librosa.feature.chroma_stft(y, sr=sr)
            tempos.append(tempo)
            tunings.append(tuning)
            zeroCrossing.append(np.mean(zcr))
            specCentroid.append(np.mean(spectral_centroids))
            specBandwidth.append(np.mean(spec_bw))
            specRolloff.append(np.mean(rolloff))
            chroma.append(np.mean(chroma_stft))
            
            counter+=1
            print(counter)
        except:
            pass
    else:
        pass

# ******** Tiny Tag Options *********
#tag.album         # album as string
#tag.albumartist   # album artist as string
#tag.artist        # artist name as string
#tag.audio_offset  # number of bytes before audio data begins
#tag.bitrate       # bitrate in kBits/s
#tag.disc          # disc number
#tag.disc_total    # the total number of discs
#tag.duration      # duration of the song in seconds
#tag.filesize      # file size in bytes
#tag.genre         # genre as string
#tag.samplerate    # samples per second
#tag.title         # title of the song
#tag.track         # track number as string
#tag.track_total   # total number of tracks as string
#tag.year          # year or data as string

MetaSongs = pd.DataFrame(
    {'artist': artist,
     'title': title,
     'album': album,
     'duration': duration,
     'year': year,
     'genre': genre,
     'audioOffset': audio_offset,
     'bitRate': bitrate,
     'sampleRate': samplerate,
     'tempo': tempos,
     'tuning': tunings,
     'ZeroCrossingRate': zeroCrossing,
     'SpectralCentroid': specCentroid,
     'SpectralBandwidth': specBandwidth,
     'SpectralRolloff': specRolloff,
     'ChromaFrequency': chroma,
    }
)

print(MetaSongs.head())

MetaSongs.to_csv('/Users/kf/Desktop/Metasongs.csv',index=True)

#Create dummy users (already created so the code is commented out)
#userid = []
#i = 0
#while i < 100:
#    userid.append(i)
#    i+=1

#Users = pd.DataFrame(
#    {'user': userid,}
#)
#Users.to_csv('/Users/kf/Desktop/Users.csv',index=False)

