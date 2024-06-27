import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load the data
df = pd.read_csv(r"C:\Users\smitp\OneDrive\Desktop\spotify_millsongdata.csv")

# Check for null values
print(df.isnull().sum())

# Sample and drop unnecessary columns
df = df.sample(5000).drop('link', axis=True).reset_index(drop=True)

# Text Cleaning / Text Preprocessing
df['text'] = df['text'].str.lower().replace(r'^\w\s', ' ', regex=True).replace(r'\n', ' ', regex=True)

# Tokenization and Stemming
nltk.download('punkt')
stemmer = PorterStemmer()

def token(txt):
    tokens = nltk.word_tokenize(txt)
    stemmed = [stemmer.stem(word) for word in tokens]
    return " ".join(stemmed)

df['text'] = df['text'].apply(lambda x: token(x))

# TF-IDF Vectorization
tfid = TfidfVectorizer(analyzer='word', stop_words='english')
matrix = tfid.fit_transform(df['text'])

# Calculate Cosine Similarity
similar = cosine_similarity(matrix)

# Recommender Function
def recommender(song_name):
    idx = df[df['song'] == song_name].index[0]
    distance = sorted(list(enumerate(similar[idx])), reverse=True, key=lambda x: x[1])
    song = []
    for s_id in distance[1:11]:
        song.append(df.iloc[s_id[0]].song)
    return song

# Save the similarity matrix and dataframe using pickle
pickle.dump(similar, open("similarity.pkl", "wb"))
pickle.dump(df, open("df.pkl", "wb"))

print("Files saved successfully!")
