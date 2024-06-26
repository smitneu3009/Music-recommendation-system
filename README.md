# Music Recommender System

This project is a music recommendation system that suggests songs based on lyrical similarity. The recommendations include song names and their album cover images. The system uses a dataset from Kaggle and leverages Natural Language Processing (NLP) techniques along with the Spotify API for fetching album covers.

## Dataset

The dataset used in this project is the [Spotify Million Song Dataset](https://www.kaggle.com/datasets/notshrirang/spotify-million-song-dataset). It contains the following columns:

- **artist**: Artist's name
- **song**: Song name
- **link**: Link to the song
- **text**: Lyrics of the song

## Project Structure

The project is structured as follows:

- `app.py`: The main application file that runs the Streamlit app.
- `spotify_millsongdata.csv`: The dataset file containing the songs and their lyrics.
- `df.pkl`: Pickle file of the processed DataFrame.
- `similarity.pkl`: Pickle file of the similarity matrix.
- `.env.clone`: Clone of the environment file to add Spotify API credentials.

## Requirements

The project requires the following Python libraries:

- pandas
- nltk
- scikit-learn
- spotipy
- streamlit
- dotenv

You can install these dependencies using pip:

```bash
pip install pandas nltk scikit-learn spotipy streamlit python-dotenv


## Preprocessing Steps

### 1. Load the Dataset
Load the dataset from the CSV file.

### 2. Text Cleaning
Convert text to lowercase and remove unnecessary characters.

### 3. Tokenization and Stemming
Tokenize the text and reduce words to their root form using the Porter Stemmer.

### 4. TF-IDF Vectorization
Convert the cleaned text data into a TF-IDF matrix.

### 5. Calculate Cosine Similarity
Compute the cosine similarity between all TF-IDF vectors.

### 6. Save Processed Data
Save the DataFrame and similarity matrix using pickle for later use.

## Running the Application

### Step 1: Set Up Spotify API Credentials
1. Rename the `.env.clone` file to `.env`.
2. Add your Spotify API credentials to the `.env` file:
    ```makefile
    CLIENT_ID=your_spotify_client_id
    CLIENT_SECRET=your_spotify_client_secret
    ```

### Step 2: Run the Streamlit App
Run the Streamlit app using the following command:
```bash
streamlit run app.py

## Step 3: Using the Recommender

1. Open the Streamlit app in your browser.
2. Select or type a song from the dropdown menu.
3. Click the "Show Recommendation" button.
4. The app will display recommended songs along with their album cover images.

## Conclusion

This project demonstrates how to build a music recommendation system using natural language processing techniques and the Spotify API. By following the steps outlined in this README, you should be able to understand the workflow, replicate the process, and run the application successfully.
