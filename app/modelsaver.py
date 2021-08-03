from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, InputLayer
from sklearn.utils import shuffle
import tensorflow_hub as hub
import pandas as pd
import os
DATASET_ENCODING = "ISO-8859-1"

df = pd.read_csv("./sentiment140.zip",encoding=DATASET_ENCODING)
df = df.iloc[:,[0,-1]]
df.columns = ['sentiment','tweet']
df = pd.concat([df.query("sentiment==0").sample(20000),df.query("sentiment==4").sample(20000)])
df.sentiment = df.sentiment.map({0:0,4:1})
df =  shuffle(df).reset_index(drop=True)

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

def vectorize(df):
    embeded_tweets = embed(df['tweet'].values.tolist()).numpy()
    targets = df.sentiment.values
    return embeded_tweets,targets

embeded_tweets,targets = vectorize(df)

model = Sequential()
model.add(InputLayer(input_shape=(512,),dtype='float32'))
model.add(Dense(128, activation = 'relu'))
model.add(Dense(64, activation = 'relu'))
model.add(Dense(1, activation = 'sigmoid'))

model.compile(loss='binary_crossentropy', 
              optimizer='adam',
              metrics=['acc'])

num_epochs = 10
batch_size = 32   ## 2^x

history = model.fit(embeded_tweets, 
                    targets, 
                    epochs=num_epochs, 
                    validation_split=0.1, 
                    shuffle=True,
                    batch_size=batch_size)

model.save(os.getcwd() + "/savedmodel")
